import { GoogleGenAI } from "@google/genai";
import type { ReviewSection, JossReview } from '../types';

const API_KEY = process.env.API_KEY;

const ai = new GoogleGenAI({ apiKey: API_KEY as string });

const parseJossReview = (markdown: string): JossReview => {
    const sections: ReviewSection[] = [];
    // Split by level 2 headings. The lookbehind `(?=## )` keeps the delimiter.
    const parts = markdown.split(/\n(?=## )/);
    let summary = "The AI couldn't generate a summary. Please check the detailed sections below.";

    for (const part of parts) {
        if (!part.trim()) continue;

        const lines = part.trim().split('\n');
        const title = lines[0].replace(/##\s*/, '').trim();
        const content = lines.slice(1).join('\n').trim();

        if (title.toLowerCase() === 'summary' || title.toLowerCase() === 'summary & key recommendations') {
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

export const generateJossReview = async (repoUrl: string): Promise<JossReview> => {
  try {
    const prompt = `
You are an expert reviewer for the Journal of Open Source Software (JOSS). Your task is to perform a pre-review of the GitHub repository at ${repoUrl} and provide constructive feedback.

Please structure your response in Markdown format. Use level 2 headings (##) for each major section.
At the very beginning of your response, provide a "## Summary & Key Recommendations" section that highlights the 3-4 most critical action items for the author to address for a successful JOSS submission.

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
