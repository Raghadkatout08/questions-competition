# questions-competition

This repository contains a serverless function that fetches trivia questions from the OpenTDB API.

## Deployed Links

- **Amount-based Queries**:
  - [20 Questions](http://localhost:3000/api/questions?amount=20): Returns `20 trivia questions with their answers`.
  - [Maximum Questions](http://localhost:3000/api/questions?amount=51): Returns `the maximum allowed number of trivia questions`.
  
- **Category-based Queries**:
  - [Sports Category](http://localhost:3000/api/questions?category=21): Returns `10 trivia questions from the Sports category`.
  - [Category 33](http://localhost:3000/api/questions?category=33): Return `You have just 32 category`.

- **General Query**:
  - [General Questions](http://localhost:3000/api/questions): Returns `Welcome to the trivia API!`.