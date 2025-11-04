import { GoogleGenAI } from "@google/genai";
import type { ReviewSection, JossReview } from "../types";

const API_KEY = process.env.API_KEY;

// Initialize AI client only if API_KEY exists
const ai = API_KEY ? new GoogleGenAI({ apiKey: API_KEY as string }) : null;

// --- MOCK DATA ---
const mockJossReview: JossReview = {
    summary: "This is a mock summary. The project looks promising but needs better documentation and more comprehensive tests before it can be accepted by JOSS. The Statement of Need is clear and compelling.",
    sections: [
        { title: "✅ 📄 Statement of Need", content: "The need for this software is well-articulated in the README. The research problem is clear, and the software provides a novel solution. This section is well done." },
        { title: "⚠️ ⚙️ Installation", content: "The installation instructions are present but could be improved. It would be beneficial to list explicit versions for dependencies in `requirements.txt` to ensure reproducibility." },
        { title: "❌ 🧪 Automated Tests", content: "No automated tests were found. JOSS requires a robust testing suite. Please add tests using a framework like `pytest` to validate the core functionality." },
        { title: "✅ 📜 License", content: "The repository contains an MIT license, which is an OSI-approved license. Great job!" },
    ],
};

const mockPrAdvice: ReviewSection[] = [
    { title: "General Advice", content: "This is mock advice. It's always a good idea to be patient, as maintainers are often busy. Double-check that your PR follows all contribution guidelines. Ensure all automated checks are passing." },
    { title: "Suggested Message", content: "Hi team, just wanted to gently follow up on this pull request. Is there any feedback I can address or any changes I can make to help move this forward? Thanks for your time!" },
];

const mockOptimizationAdvice: ReviewSection[] = [
    { title: "🏛️ Architectural Suggestions", content: "Mock Suggestion: Consider creating a dedicated `src/` directory for your main Python package to better separate it from configuration files and tests. This is a common pattern in projects like `scikit-learn` and `pandas`." },
    { title: "✨ Readability & Pythonic Idioms", content: "Mock Suggestion: Replace traditional `for` loops for list creation with more concise and efficient list comprehensions.\n```python\n# Before\nnew_list = []\nfor item in old_list:\n  if item.is_valid():\n    new_list.append(item.process())\n\n# After\nnew_list = [item.process() for item in old_list if item.is_valid()]\n```" },
    { title: "⚡️ Performance Optimizations", content: "Mock Suggestion: For numerical computations, ensure you are using NumPy vectorization instead of iterating over arrays in Python. This can lead to significant speedups." },
];


const parseJossReview = (markdown: string): JossReview => {
    const sections: ReviewSection[] = [];
    const parts = markdown.split(/\n(?=## )/);
    let summary = "The AI couldn't generate a summary. Please check the detailed sections below.";

    for (const part of parts) {
        if (!part.trim()) continue;

        const lines = part.trim().split('\n');
        const title = lines[0].replace(/##\s*/, '').trim();
        const content = lines.slice(1).join('\n').trim();

        if (title.toLowerCase() === 'summary') {
            summary = content;
        } else if (title && content) {
            sections.push({ title, content });
        }
    }
    return { summary, sections };
};

const parseMarkdownIntoSections = (markdown: string): ReviewSection[] => {
    const sections: ReviewSection[] = [];
    const parts = markdown.split(/\n(?=## )/);

    for (const part of parts) {
        if (!part.trim()) continue;
        const lines = part.trim().split('\n');
        const title = lines[0].replace(/##\s*/, '').trim();
        const content = lines.slice(1).join('\n').trim();
        if (title && content) {
            sections.push({ title, content });
        }
    }
    return sections;
};

// --- API FUNCTIONS with Mock Fallback ---

const simulateDelay = <T>(data: T): Promise<T> => 
    new Promise(resolve => setTimeout(() => resolve(data), 1500));

export const generateJossReview = async (repoUrl: string): Promise<JossReview> => {
  if (!ai) {
    console.log("Using mock data for JOSS review.");
    return simulateDelay(mockJossReview);
  }
  try {
    const prompt = `
You are an expert reviewer for the Journal of Open Source Software (JOSS). Your task is to perform a pre-review of the GitHub repository at ${repoUrl} and provide constructive feedback.

Please structure your response in Markdown format. Use level 2 headings (##) for each major section.
At the very beginning of your response, provide a "## Summary" section that highlights the 3-4 most critical action items for the author to address for a successful JOSS submission.

For each detailed section below, provide a brief status emoji (✅ Good, ⚠️ Improvement needed, ❌ Missing) followed by a detailed analysis and actionable recommendations.

Here are the sections to cover:
## 📄 Statement of Need
- Does the paper.md or README clearly explain the research problem and why this software is a solution?

## ⚙️ Installation
- Are the installation instructions clear and complete?

## 📖 Example Usage
- Is there a clear, working example of how to use the software?

## 📚 Functionality
- Does the software do what it claims to do?

## 📝 Documentation
- Is there a high-level documentation page or a comprehensive README?
- Is the API documentation clear?

## 🧪 Automated Tests
- Are there automated tests for the software?

## 🤝 Community Guidelines
- Is there a \`CONTRIBUTING.md\` file and a Code of Conduct?

## 📜 License
- Is there a license file and is it an OSI-approved license?

## 📄 Software Paper (paper.md)
- Is there a \`paper.md\` file and does it follow the JOSS paper structure?
`;

    const response = await ai.models.generateContent({
        model: 'gemini-2.5-pro',
        contents: prompt,
    });

    const reviewText = (response as any).text;
    if (!reviewText) {
        throw new Error("Received an empty response from the API.");
    }

    return parseJossReview(reviewText);

  } catch (error) {
    console.error("Error generating JOSS review:", error);
    if (error instanceof Error) {
        throw new Error(`Failed to generate review: ${error.message}`);
    }
    throw new Error("An unknown error occurred while generating the review.");
  }
};

export const generatePrFollowupAdvice = async (prUrl: string): Promise<ReviewSection[]> => {
    if (!ai) {
        console.log("Using mock data for PR advice.");
        return simulateDelay(mockPrAdvice);
    }
    try {
        const prompt = `
You are an experienced and friendly open-source maintainer. A contributor is asking for advice on how to follow up on a GitHub pull request that has not received any comments for over a week. The PR is located at: ${prUrl}.

Please provide clear, actionable, and encouraging advice. Structure your response in Markdown.

Use level 2 headings (##) for each section. Create the following sections:
## General Advice
Provide best practices like exercising patience, double-checking the project's contributing guidelines for communication protocols, and ensuring the PR is in good shape (e.g., passes all checks, is not a draft, has a clear description).

## Suggested Message
Provide a polite and concise message template the contributor can post on the pull request to gently bump the thread. The message should be friendly and offer to make any necessary changes. For example: "Hi maintainers, I just wanted to gently follow up on this PR. Please let me know if there are any changes I can make to help with the review process. Thank you for your time and for maintaining this great project!"
`;
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: prompt,
        });

        const adviceText = (response as any).text;
        if (!adviceText) {
            throw new Error("Received an empty response from the API.");
        }
        return parseMarkdownIntoSections(adviceText);
    } catch (error) {
        console.error("Error generating PR advice:", error);
        if (error instanceof Error) {
            throw new Error(`Failed to generate advice: ${error.message}`);
        }
        throw new Error("An unknown error occurred while generating the advice.");
    }
};

export const generateCodeOptimizationAdvice = async (repoUrl: string): Promise<ReviewSection[]> => {
    if (!ai) {
        console.log("Using mock data for code optimization.");
        return simulateDelay(mockOptimizationAdvice);
    }
    try {
        const prompt = `
You are a world-class senior software engineer and open-source contributor with deep expertise in Python, code architecture, and performance optimization. Your task is to conduct a comprehensive code review and optimization analysis for the GitHub repository at ${repoUrl}.

The repository is for 'Circular Bias Detection' (CBD).

First, identify 2-3 popular, high-quality open-source Python projects that are similar in scope or domain (e.g., scientific computing, data analysis, machine learning fairness/bias detection). Compare the code structure, patterns, and best practices from those projects against the provided repository.

Then, provide actionable code optimization suggestions for the CBD project. Structure your response in Markdown. Use level 2 headings (##) for each major optimization category. For each suggestion, provide a brief explanation of the 'why' (e.g., for performance, readability, or maintainability) and, where possible, a short code snippet to illustrate the improvement.

Please cover the following categories:

## 🏛️ Architectural Suggestions
Analyze module organization, separation of concerns, and overall project structure.

## ✨ Readability & Pythonic Idioms
Suggest improvements using Pythonic idioms like list comprehensions, context managers, etc.

## ⚡️ Performance Optimizations
Identify potential bottlenecks and suggest performance improvements, such as vectorization with NumPy or using more efficient data structures.

## 📦 Dependency Management
Review the dependency management (e.g., requirements.txt) and suggest best practices like using pyproject.toml and poetry/pip-tools.

## 🧪 Testing Strategy
Analyze the testing setup and suggest improvements, like using pytest fixtures, parameterization, or increasing coverage of critical logic.
`;
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-pro',
            contents: prompt,
        });

        const adviceText = (response as any).text;
        if (!adviceText) {
            throw new Error("Received an empty response from the API.");
        }
        return parseMarkdownIntoSections(adviceText);
    } catch (error) {
        console.error("Error generating code optimization advice:", error);
        if (error instanceof Error) {
            throw new Error(`Failed to generate advice: ${error.message}`);
        }
        throw new Error("An unknown error occurred while generating the advice.");
    }
};
