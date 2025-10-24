"""
Machine Learning-based bias detection.

This module implements ML-powered bias detection using:
- XGBoost classifier with SHAP explainability
- Ensemble methods combining statistical and ML approaches
- Feature engineering from time series data
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, List
import warnings

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    warnings.warn("xgboost not installed. Install with: pip install xgboost")

try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    warnings.warn("scikit-learn not installed. Install with: pip install scikit-learn")


class MLBiasDetector:
    """
    Machine Learning-based circular bias detector.
    
    Uses XGBoost classifier trained on features extracted from
    evaluation time series data.
    
    Attributes:
    -----------
    model : xgb.XGBClassifier
        Trained XGBoost model
    scaler : StandardScaler
        Feature scaler
    feature_names : list
        Names of extracted features
    """
    
    def __init__(self):
        if not HAS_XGBOOST or not HAS_SKLEARN:
            raise ImportError("MLBiasDetector requires xgboost and scikit-learn")
        
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.is_trained = False
        
    def extract_features(self, 
                        performance_matrix: np.ndarray,
                        constraint_matrix: np.ndarray) -> np.ndarray:
        """
        Extract feature vector from evaluation data.
        
        Combines statistical indicators, time series features,
        and advanced metrics.
        
        Parameters:
        -----------
        performance_matrix : np.ndarray, shape (T, K)
        constraint_matrix : np.ndarray, shape (T, p)
        
        Returns:
        --------
        np.ndarray, shape (n_features,)
            Feature vector
        """
        from .core import compute_psi, compute_ccs, compute_rho_pc
        from .advanced_metrics import (compute_tdi, compute_ics, 
                                       compute_ads, compute_mci)
        from scipy import stats as sp_stats
        
        features = []
        
        # ===== 1. Core Statistical Indicators =====
        try:
            psi = compute_psi(performance_matrix)
            ccs = compute_ccs(constraint_matrix)
            rho_pc = compute_rho_pc(performance_matrix, constraint_matrix)
        except Exception as e:
            warnings.warn(f"Error computing core metrics: {e}")
            psi, ccs, rho_pc = 0.0, 0.0, 0.0
        
        features.extend([psi, ccs, rho_pc])
        
        # ===== 2. Advanced Metrics =====
        try:
            tdi = compute_tdi(performance_matrix)
            ics = compute_ics(performance_matrix, constraint_matrix)
            ads = compute_ads(performance_matrix, constraint_matrix)
            mci, _ = compute_mci(constraint_matrix)
        except Exception as e:
            warnings.warn(f"Error computing advanced metrics: {e}")
            tdi, ics, ads, mci = 0.0, 0.0, 0.0, 0.0
        
        features.extend([tdi, ics, ads, mci])
        
        # ===== 3. Time Series Features =====
        perf_mean = performance_matrix.mean(axis=1)
        
        # Trend
        if len(perf_mean) > 1:
            perf_trend = np.polyfit(range(len(perf_mean)), perf_mean, 1)[0]
        else:
            perf_trend = 0.0
        
        # Volatility
        perf_volatility = np.std(np.diff(perf_mean)) if len(perf_mean) > 1 else 0.0
        
        # Acceleration
        if len(perf_mean) > 2:
            perf_accel = np.polyfit(range(len(perf_mean)), perf_mean, 2)[0]
        else:
            perf_accel = 0.0
        
        features.extend([perf_trend, perf_volatility, perf_accel])
        
        # ===== 4. Constraint Features =====
        const_mean = constraint_matrix.mean(axis=1)
        
        # Range
        constraint_range = np.ptp(constraint_matrix, axis=0).mean()
        
        # Trend
        if len(const_mean) > 1:
            const_trend = np.polyfit(range(len(const_mean)), const_mean, 1)[0]
        else:
            const_trend = 0.0
        
        # Volatility
        const_volatility = np.std(np.diff(const_mean)) if len(const_mean) > 1 else 0.0
        
        features.extend([constraint_range, const_trend, const_volatility])
        
        # ===== 5. Performance-Constraint Interactions =====
        # Covariance
        if len(perf_mean) > 1:
            perf_const_cov = np.cov(perf_mean, const_mean)[0, 1]
        else:
            perf_const_cov = 0.0
        
        # Lagged correlation (performance leads constraint)
        if len(perf_mean) > 2:
            lag1_corr = np.corrcoef(perf_mean[:-1], const_mean[1:])[0, 1]
        else:
            lag1_corr = 0.0
        
        features.extend([perf_const_cov, lag1_corr])
        
        # ===== 6. Distribution Features =====
        # Skewness and kurtosis
        perf_flat = performance_matrix.flatten()
        perf_skewness = sp_stats.skew(perf_flat)
        perf_kurtosis = sp_stats.kurtosis(perf_flat)
        
        features.extend([perf_skewness, perf_kurtosis])
        
        # ===== 7. Algorithmic Diversity Features =====
        # Variance across algorithms
        alg_variance = np.mean(np.var(performance_matrix, axis=1))
        
        # Range across algorithms
        alg_range = np.mean(np.ptp(performance_matrix, axis=1))
        
        features.extend([alg_variance, alg_range])
        
        # Define feature names
        if self.feature_names is None:
            self.feature_names = [
                'psi', 'ccs', 'rho_pc',
                'tdi', 'ics', 'ads', 'mci',
                'perf_trend', 'perf_volatility', 'perf_accel',
                'constraint_range', 'const_trend', 'const_volatility',
                'perf_const_cov', 'lag1_corr',
                'perf_skewness', 'perf_kurtosis',
                'alg_variance', 'alg_range'
            ]
        
        return np.array(features)
    
    def train(self, 
              X_train: np.ndarray, 
              y_train: np.ndarray,
              X_val: Optional[np.ndarray] = None,
              y_val: Optional[np.ndarray] = None):
        """
        Train the ML model.
        
        Parameters:
        -----------
        X_train : np.ndarray, shape (n_samples, n_features)
            Training features
        y_train : np.ndarray, shape (n_samples,)
            Training labels (0=no bias, 1=bias)
        X_val : np.ndarray, optional
            Validation features
        y_val : np.ndarray, optional
            Validation labels
        """
        # Initialize scaler
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Initialize model
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            min_child_weight=1,
            subsample=0.8,
            colsample_bytree=0.8,
            objective='binary:logistic',
            eval_metric='auc',
            random_state=42,
            use_label_encoder=False
        )
        
        # Train
        if X_val is not None and y_val is not None:
            X_val_scaled = self.scaler.transform(X_val)
            eval_set = [(X_train_scaled, y_train), (X_val_scaled, y_val)]
            self.model.fit(
                X_train_scaled, y_train,
                eval_set=eval_set,
                verbose=False
            )
        else:
            self.model.fit(X_train_scaled, y_train)
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, 
            cv=5, scoring='roc_auc'
        )
        
        print(f"Training completed.")
        print(f"Cross-validation AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        self.is_trained = True
    
    def predict(self, X_test: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict bias labels and probabilities.
        
        Parameters:
        -----------
        X_test : np.ndarray, shape (n_samples, n_features)
            Test features
            
        Returns:
        --------
        predictions : np.ndarray, shape (n_samples,)
            Class predictions (0/1)
        probabilities : np.ndarray, shape (n_samples,)
            Bias probabilities
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        X_test_scaled = self.scaler.transform(X_test)
        predictions = self.model.predict(X_test_scaled)
        probabilities = self.model.predict_proba(X_test_scaled)[:, 1]
        
        return predictions, probabilities
    
    def explain(self, X: np.ndarray, sample_idx: int = 0):
        """
        Explain prediction using SHAP values.
        
        Parameters:
        -----------
        X : np.ndarray, shape (n_samples, n_features)
            Features to explain
        sample_idx : int
            Sample index to explain
            
        Returns:
        --------
        dict
            Explanation dictionary with SHAP values and feature importance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before explanation")
        
        try:
            import shap
        except ImportError:
            warnings.warn("SHAP not installed. Install with: pip install shap")
            return self._fallback_explain(X, sample_idx)
        
        X_scaled = self.scaler.transform(X)
        
        # SHAP explainer
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X_scaled)
        
        # Extract explanation for specific sample
        if isinstance(shap_values, list):
            shap_values_sample = shap_values[1][sample_idx]  # Positive class
        else:
            shap_values_sample = shap_values[sample_idx]
        
        # Sort by absolute importance
        feature_importance = list(zip(
            self.feature_names,
            shap_values_sample,
            X[sample_idx]
        ))
        feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
        
        return {
            'shap_values': shap_values_sample,
            'feature_importance': feature_importance,
            'base_value': explainer.expected_value,
            'prediction': self.model.predict_proba(X_scaled[sample_idx:sample_idx+1])[0, 1]
        }
    
    def _fallback_explain(self, X: np.ndarray, sample_idx: int) -> dict:
        """Fallback explanation using feature importance."""
        # Use XGBoost feature importance
        importance = self.model.feature_importances_
        
        feature_importance = list(zip(
            self.feature_names,
            importance,
            X[sample_idx]
        ))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'feature_importance': feature_importance,
            'explanation_method': 'xgboost_importance'
        }
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance ranking.
        
        Returns:
        --------
        pd.DataFrame
            Feature importance dataframe
        """
        if not self.is_trained:
            raise ValueError("Model must be trained")
        
        importance = self.model.feature_importances_
        
        df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': importance
        })
        df = df.sort_values('importance', ascending=False)
        
        return df


class EnsembleBiasDetector:
    """
    Ensemble detector combining statistical and ML approaches.
    
    Combines the strengths of rule-based statistical detection
    and data-driven machine learning.
    """
    
    def __init__(self, 
                 statistical_weight: float = 0.6,
                 ml_weight: float = 0.4):
        """
        Initialize ensemble detector.
        
        Parameters:
        -----------
        statistical_weight : float
            Weight for statistical detector (default: 0.6)
        ml_weight : float
            Weight for ML detector (default: 0.4)
        """
        from .detection import BiasDetector
        
        self.statistical_detector = BiasDetector()
        self.ml_detector = MLBiasDetector()
        
        # Normalize weights
        total = statistical_weight + ml_weight
        self.weights = {
            'statistical': statistical_weight / total,
            'ml': ml_weight / total
        }
    
    def detect_bias(self,
                   performance_matrix: np.ndarray,
                   constraint_matrix: np.ndarray,
                   algorithm_names: Optional[List[str]] = None) -> Dict:
        """
        Ensemble bias detection.
        
        Parameters:
        -----------
        performance_matrix : np.ndarray, shape (T, K)
        constraint_matrix : np.ndarray, shape (T, p)
        algorithm_names : list, optional
            
        Returns:
        --------
        dict
            Comprehensive detection results
        """
        # 1. Statistical detection
        stat_results = self.statistical_detector.detect_bias(
            performance_matrix, 
            constraint_matrix,
            algorithm_names=algorithm_names
        )
        stat_score = stat_results['confidence']
        
        # 2. ML detection
        if self.ml_detector.is_trained:
            features = self.ml_detector.extract_features(
                performance_matrix, constraint_matrix
            ).reshape(1, -1)
            _, ml_prob = self.ml_detector.predict(features)
            ml_score = ml_prob[0]
        else:
            warnings.warn("ML detector not trained, using statistical only")
            ml_score = stat_score
            self.weights['statistical'] = 1.0
            self.weights['ml'] = 0.0
        
        # 3. Weighted ensemble
        ensemble_score = (
            self.weights['statistical'] * stat_score +
            self.weights['ml'] * ml_score
        )
        
        # 4. Decision
        bias_detected = ensemble_score > 0.5
        
        # 5. Confidence calibration
        # Higher agreement between methods = higher confidence
        agreement = 1 - abs(stat_score - ml_score)
        calibrated_confidence = ensemble_score * (0.5 + 0.5 * agreement)
        
        return {
            'bias_detected': bias_detected,
            'ensemble_score': ensemble_score,
            'calibrated_confidence': calibrated_confidence,
            'statistical_score': stat_score,
            'ml_score': ml_score,
            'method_agreement': agreement,
            'weights': self.weights,
            'statistical_details': stat_results
        }
