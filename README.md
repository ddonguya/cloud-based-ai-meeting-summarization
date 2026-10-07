An AWS-based AI meeting summarization application using Amazon Transcribe, External AI (Gemini 3.5 Flash Lite), AWS Lambda, and Amazon S3 to transform recorded meetings into structured summaries and actionable insights.

Project Status: In Development

Overview

The goal of this project is to build a cloud-based application that helps users quickly understand and organize information from recorded meetings.

The application will process meeting recordings and generate:

Meeting summaries Key discussion points Decisions made Action items Other relevant meeting insights Architecture Meeting Audio/Video │ ▼ Amazon S3 │ ▼ Amazon Transcribe │ ▼ Transcript (JSON) │ ▼ AWS Lambda │ ▼ Gemini 3.5 Flash Lite │ ▼ AI-Generated Summary │ ▼ Amazon S3

AWS Services Service Purpose

Amazon S3 Stores meeting recordings, transcripts, and generated summaries
Amazon Transcribe Converts meeting audio/video into text
AWS Lambda Processes transcripts and orchestrates the workflow
Gemini 3.5 Flash Lite Provides access to foundation models for AI-powered transcript analysis and summarization
