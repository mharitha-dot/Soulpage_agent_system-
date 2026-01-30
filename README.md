# Soulpage_agent_system-
Agentic AI System with two or more collaborating agents to perform a multi-step task 
Multi-Agent Company Intelligence System

This project implements a Multi-Agent AI System using LangChain, developed as part of a technical assignment to demonstrate agent orchestration, context management, and multi-step reasoning through collaborating AI agents.

System Architecture
User
  ↓
Orchestrator / Controller Agent
  ↓
Data Collector Agent
  ↓
Analyst Agent
  ↓
Final Company Intelligence Report

Architecture Description

The Orchestrator Agent manages the overall workflow and coordinates communication between agents.

The Data Collector Agent gathers company-related information using external sources or dummy data.

The Analyst Agent processes the collected data to generate summaries, insights, and potential risk factors.

The system maintains shared context between agents to enable structured, multi-step decision-making and insight generation.
