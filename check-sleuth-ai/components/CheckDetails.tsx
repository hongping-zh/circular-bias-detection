
import React from 'react';
import type { CheckData } from '../types';

interface InputFieldProps {
  label: string;
  id: keyof CheckData;
  value: string | boolean;
  onChange: (id: keyof CheckData, value: string | boolean) => void;
  type?: string;
  isLoading: boolean;
}

const InputField: React.FC<InputFieldProps> = ({ label, id, value, onChange, type = 'text', isLoading }) => {
    if (isLoading) {
        return (
            <div>
                <label className="block text-sm font-medium text-slate-400">{label}</label>
                <div className="mt-1 h-10 w-full animate-pulse rounded-md bg-slate-700"></div>
            </div>
        )
    }
  
    if (type === 'checkbox') {
    return (
      <div className="flex items-center justify-between bg-slate-800 p-3 rounded-md border border-slate-700">
        {/* Fix: Ensure 'id' is a string for the 'htmlFor' attribute. */}
        <label htmlFor={String(id)} className="block text-sm font-medium text-slate-300">
          {label}
        </label>
        <div className={`w-6 h-6 rounded flex items-center justify-center ${value ? 'bg-blue-600' : 'bg-slate-600'}`}>
            {value && <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" /></svg>}
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Fix: Ensure 'id' is a string for the 'htmlFor' attribute. */}
      <label htmlFor={String(id)} className="block text-sm font-medium text-slate-400">
        {label}
      </label>
      <input
        type={type}
        // Fix: Ensure 'id' is a string for the 'name' attribute.
        name={String(id)}
        // Fix: Ensure 'id' is a string for the 'id' attribute.
        id={String(id)}
        value={String(value)}
        onChange={(e) => onChange(id, e.target.value)}
        className="mt-1 block w-full bg-slate-700 border-slate-600 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm h-10 px-3"
      />
    </div>
  );
};

interface CheckDetailsProps {
  data: CheckData | null;
  onDataChange: (data: CheckData) => void;
  isLoading: boolean;
}

export const CheckDetails: React.FC<CheckDetailsProps> = ({ data, onDataChange, isLoading }) => {
  const handleChange = (id: keyof CheckData, value: string | boolean) => {
    if (data) {
      onDataChange({ ...data, [id]: value });
    }
  };
  
  const loadingData: CheckData = { payee: '', amountNumeric: '', amountText: '', date: '', memo: '', routingNumber: '', accountNumber: '', checkNumber: '', signatureDetected: false };
  const displayData = data || loadingData;

  return (
    <div className="bg-slate-800 p-6 rounded-lg border border-slate-700 shadow-lg">
      <h2 className="text-2xl font-bold text-slate-300 mb-4">Extracted Details</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="md:col-span-2">
            <InputField label="Payee" id="payee" value={displayData.payee} onChange={handleChange} isLoading={isLoading}/>
        </div>
        <InputField label="Amount (Numeric)" id="amountNumeric" value={displayData.amountNumeric} onChange={handleChange} isLoading={isLoading}/>
        <div className="md:col-span-2">
            <InputField label="Amount (Text)" id="amountText" value={displayData.amountText} onChange={handleChange} isLoading={isLoading}/>
        </div>
        <InputField label="Date" id="date" value={displayData.date} onChange={handleChange} isLoading={isLoading}/>
        <InputField label="Check Number" id="checkNumber" value={displayData.checkNumber} onChange={handleChange} isLoading={isLoading}/>
        <div className="md:col-span-2">
            <InputField label="Memo" id="memo" value={displayData.memo} onChange={handleChange} isLoading={isLoading}/>
        </div>
        <InputField label="Routing Number" id="routingNumber" value={displayData.routingNumber} onChange={handleChange} isLoading={isLoading}/>
        <InputField label="Account Number" id="accountNumber" value={displayData.accountNumber} onChange={handleChange} isLoading={isLoading}/>
        <div className="md:col-span-2">
             <InputField label="Signature Detected" id="signatureDetected" type="checkbox" value={displayData.signatureDetected} onChange={handleChange} isLoading={isLoading}/>
        </div>
      </div>
    </div>
  );
};