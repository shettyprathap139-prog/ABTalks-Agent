# ABTalks Agent

An autonomous AI-powered security intelligence agent that discovers recent cybersecurity and AI-security news, evaluates its relevance, generates insightful posts, and stores published content with persistent memory.

## Overview

ABTalks Agent automates the process of turning security news into useful technical posts.

The system:

1. Fetches recent articles from trusted RSS feeds.
2. Filters articles for security relevance and freshness.
3. Checks whether an article has already been published.
4. Uses Gemini to rank relevant articles.
5. Generates a concise technical post.
6. Stores the post in SQLite.
7. Saves publishing context to Breeth memory.
8. Exposes the generated posts through a FastAPI API.
9. Runs autonomously on a configurable interval.

## Architecture

```text
RSS News Sources
       |
       v
News Fetcher
       |
       v
Security Relevance Filter
       |
       v
Duplicate Detection
       |
       v
Gemini Article Ranking
       |
       v
AI Post Writer
       |
       +-----------> Breeth Memory
       |
       v
SQLite Database
       |
       v
FastAPI
       |
       v
Web Frontend