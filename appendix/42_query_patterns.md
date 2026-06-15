# MeetAll: 42 Enterprise Query Patterns

## Overview

This document describes the **42 query patterns** identified through stakeholder interviews with **15 enterprise professionals** across **3 sectors** (finance, healthcare, technology) and **4 roles** (product manager, engineer, compliance officer, executive). These patterns form the foundation of the MeetAll benchmark's multi-dimensional complexity annotation.

## Four-Dimensional Taxonomy

### Dimension 1: Cognitive Load (CL)

| Level | Operational Definition | Response Time |
|-------|----------------------|---------------|
| **Low** | Direct fact extraction from explicit mentions | <5 seconds |
| **Medium** | Synthesis across 2-5 utterances or simple reasoning | 15-30 seconds |
| **High** | Multi-hop inference, causal reasoning, or complex synthesis | >45 seconds |

**Examples by CL level:**
- **Low**: "What time does the meeting start tomorrow?"
- **Medium**: "Summarize the main points discussed in the last 10 minutes"
- **High**: "Based on the technical discussion, will this architecture scale to 100k concurrent users?"

### Dimension 2: Context Dependency (CD)

| Level | Definition |
|-------|------------|
| **None** | Query is self-contained; no meeting context required for understanding |
| **Recent** | References the last 3-5 utterances of current conversation |
| **Long-range** | References content from 15+ minutes earlier in same meeting |
| **Cross-meeting** | References content from prior meeting sessions |

**Examples by CD level:**
- **None**: "What is GDPR?" (general knowledge)
- **Recent**: "Who just mentioned the deadline?"
- **Long-range**: "Earlier you mentioned a bug fix - what was the resolution?"
- **Cross-meeting**: "In last week's meeting, we decided on X - has that been implemented?"

### Dimension 3: Domain Knowledge (DK)

| Level | Required Knowledge |
|-------|-------------------|
| **General** | Common sense knowledge only |
| **Basic** | Field-specific terminology (e.g., "sprint", "QBR", "compliance") |
| **Expert** | Deep technical/regulatory expertise (e.g., HIPAA requirements, system architecture) |

**Examples by DK level:**
- **General**: "How many people are in this meeting?"
- **Basic**: "Is this feature in scope for Q3 sprint?"
- **Expert**: "Does this data pipeline design comply with CCPA Article 7?"

### Dimension 4: Task-Execution Effort (TE)

| Level | Action Required |
|--------|-----------------|
| **Low** | Passive recording (e.g., note-taking) |
| **Medium** | Structured organization (e.g., summarizing action items) |
| **High** | Strategic planning with tool calls (e.g., cross-meeting aggregation, web search) |

---

## The 42 Query Patterns

The following 42 patterns are organized by their primary dimension emphasis. Each pattern includes an example query and its dimensional annotation.

### Category A: Fact Retrieval & Verification (CL=Low, CD=Varies)

| ID | Pattern Name | Example Query | CL | CD | DK | TE |
|----|-------------|---------------|----|----|----|-----|
| A1 | **Time/Date Extraction** | "When is the next team standup scheduled?" | Low | None | General | Low |
| A2 | **Participant Identification** | "Who is leading today's compliance review?" | Low | Recent | General | Low |
| A3 | **Decision Confirmation** | "Did we approve the budget increase?" | Low | Recent | Basic | Low |
| A4 | **Number/Figure Lookup** | "What was the Q1 revenue number?" | Low | Long-range | Basic | Low |
| A5 | **Status Check** | "Is the API migration complete?" | Low | Long-range | Basic | Low |
| A6 | **Action Item Owner** | "Who owns the documentation task?" | Low | Recent | General | Low |
| A7 | **Location/Venue** | "Where is the client meeting happening?" | Low | None | General | Low |
| A8 | **Agenda Item Recall** | "What's item #3 on today's agenda?" | Low | None | General | Low |
| A9 | **Deadline Verification** | "When is the regulatory filing due?" | Low | Long-range | Basic | Low |
| A10 | **Attendance Count** | "How many people joined the morning sync?" | Low | Recent | General | Low |
| A11 | **Document Reference** | "Which doc contains the API specs?" | Low | Long-range | Basic | Low |

### Category B: Contextual Understanding (CL=Medium, CD=Recent/Long-range)

| ID | Pattern Name | Example Query | CL | CD | DK | TE |
|----|-------------|---------------|----|----|----|-----|
| B1 | **Recent Summary** | "Can you summarize what we just discussed about the timeline?" | Medium | Recent | Basic | Medium |
| B2 | **Speaker Intent** | "Why did Sarah bring up the security issue?" | Medium | Recent | Basic | Medium |
| B3 | **Consensus Detection** | "Did everyone agree on the approach?" | Medium | Recent | General | Medium |
| B4 | **Conflict Identification** | "What was the disagreement about earlier?" | Medium | Long-range | Basic | Medium |
| B5 | **Progress Update** | "Where do we stand on the integration work?" | Medium | Long-range | Basic | Medium |
| B6 | **Reasoning Chain** | "What led us to choose solution A over B?" | Medium | Long-range | Basic | Medium |
| B7 | **Sentiment Assessment** | "How did the client react to our proposal?" | Medium | Recent | General | Medium |
| B8 | **Key Takeaway Extraction** | "What were the three main outcomes from this session?" | Medium | Long-range | Basic | Medium |
| B9 | **Issue Escalation Status** | "Has the production issue been escalated?" | Medium | Recent | Basic | Medium |
| B10 | **Resource Allocation** | "Who's working on what this sprint?" | Medium | Long-range | Basic | Medium |
| B11 | **Dependency Mapping** | "What blocks us from starting the frontend work?" | Medium | Long-range | Basic | Medium |

### Category C: Complex Reasoning & Inference (CL=High)

| ID | Pattern Name | Example Query | CL | CD | DK | TE |
|----|-------------|---------------|----|----|----|-----|
| C1 | **Causal Analysis** | "If we delay the launch, what's the impact on Q3 targets?" | High | Long-range | Expert | High |
| C2 | **Trade-off Evaluation** | "Given the cost constraints, should we prioritize speed or accuracy?" | High | Long-range | Expert | High |
| C3 | **Hypothesis Testing** | "Will this fix actually resolve the memory leak root cause?" | High | Recent | Expert | High |
| C4 | **Gap Analysis** | "What's missing between our current state and compliance requirements?" | High | Long-range | Expert | High |
| C5 | **Risk Assessment** | "What's the probability this architectural change causes downtime?" | High | Long-range | Expert | High |
| C6 | **Scenario Simulation** | "If user traffic doubles during Black Friday, can our system handle it?" | High | Long-range | Expert | High |
| C7 | **Root Cause Analysis** | "Why have we been seeing increased latency since last deployment?" | High | Long-range | Expert | High |
| C8 | **Strategic Alignment** | "Does this feature request align with our Q4 roadmap priorities?" | High | Long-range | Basic | High |
| C9 | **Cost-Benefit Analysis** | "Is the ROI positive if we invest in the new monitoring tool?" | High | Long-range | Expert | High |
| C10 | **Compliance Impact** | "How does this data handling change affect our GDPR obligations?" | High | Long-range | Expert | High |

### Category D: Cross-Meeting Queries (CD=Cross-meeting)

| ID | Pattern Name | Example Query | CL | CD | DK | TE |
|----|-------------|---------------|----|----|----|-----|
| D1 | **Decision Tracking** | "In last week's meeting, we decided X - has that been implemented?" | Medium | Cross-meeting | Basic | Medium |
| D2 | **Trend Analysis** | "How has the customer complaint rate changed over the past month's meetings?" | High | Cross-meeting | Expert | High |
| D3 | **Commitment Follow-up** | "Who committed to deliver the prototype in the March 1st meeting? What's the status?" | Medium | Cross-meeting | Basic | Medium |
| D4 | **Pattern Recognition** | "Across the last 3 meetings, what recurring issues keep coming up?" | High | Cross-meeting | Expert | High |
| D5 | **Stakeholder Consistency** | "Did the VP agree with the direction set in the previous leadership meeting?" | Medium | Cross-meeting | Basic | Medium |
| D6 | **Timeline Correlation** | "When did we first identify this risk, and how has the mitigation plan evolved?" | High | Cross-meeting | Expert | High |
| D7 | **Knowledge Transfer** | "What did the previous team decide about the legacy system migration?" | Medium | Cross-meeting | Basic | Medium |
| D8 | **Action Item Audit** | "Of all action items assigned in the last sprint review, which ones remain open?" | High | Cross-meeting | Basic | High |
| D9 | **Context Continuity** | "Before diving into today's topic, can we recap where we left off last Tuesday?" | Medium | Cross-meeting | General | Medium |
| D10 | **Multi-Meeting Aggregation** | "Combine the feedback from the last three customer meetings into one summary." | High | Cross-meeting | Expert | High |

---

## 13 Consolidated Classes

The 108 Cartesian cells (3×4×3×3) are consolidated into 13 representative classes based on enterprise frequency distribution and error correlation analysis:

| Class | Description | % in Dataset | Example Patterns |
|-------|------------|--------------|------------------|
| **C01** | Simple fact-check (Low-CL, No-CD) | ~15% | A1-A11 |
| **C02** | Recent context summary (Med-CL, Rec-CD) | ~12% | B1, B3, B7, B9 |
| **C03** | Long-range recall (Med-CL, Lrg-CD) | ~11% | B4, B5, B8, B10, B11 |
| **C04** | Domain-basic reasoning (Med-CL, Bas-DK) | ~10% | B2, B6, D1, D3, D5, D7, D9 |
| **C05** | Expert domain inference (Hi-CL, Exp-DK) | ~10% | C1-C10 |
| **C06** | Cross-meeting tracking (Any-CL, Crs-CD) | ~15% | D1-D10 |
| **C07** | Strategic decision support (Hi-CL, Hi-TE) | ~8% | C2, C8, C9 |
| **C08** | Compliance & risk (Hi-CL, Exp-DK, Crs-CD) | ~5% | C4, C10, D4, D6, D10 |
| **C09** | Technical deep-dive (Hi-CL, Exp-DK) | ~7% | C3, C5, C6, C7 |
| **C10** | Project status synthesis (Med-CL, Med-TE) | ~8% | B5, B8, D3, D8 |
| **C11** | Meeting facilitation (Low-CL, Med-TE) | ~4% | B1, B3, B7 |
| **C12** | Resource coordination (Med-CL, Med-TE) | ~3% | B10, B11 |
| **C13** | Executive overview (Hi-CL, Any-CD, Hi-TE) | ~2% | C2, C8, D4, D10 |

---

## Usage in Benchmark Construction

### Query Generation Process

1. **Sampling**: For each 5-minute meeting segment, sample a complexity class following enterprise frequency distribution
2. **Prompting**: Use GPT-4o/DeepSeek-R1 with 5k-token context window to generate candidate queries matching the sampled class
3. **Validation**: 5 domain experts validate each query on adequacy, faithfulness, applicability (4-point Likert, κ=0.82)
4. **Refinement**: Queries rated <2 are regenerated; final ground truth is human-curated

### Annotation Schema

Each query record includes:
```json
{
  "question": "Query text",
  "final_answer": "Gold answer",
  "language": "en" | "zh",
  "split": "train" | "dev" | "test",
  "meeting_id": "Source meeting identifier",
  "labels": {
    "CL": "low" | "medium" | "high",
    "CD": "none" | "recent" | "long_range" | "cross_meeting",
    "DK": "general" | "basic" | "expert",
    "TE": "low" | "medium" | "high",
    "class13": "C01" | "C02" | ... | "C13"
  },
  "evidence": ["Supporting transcript spans"],
  "cross_meeting_refs": [{"meeting_id": "...", "segment_id": "..."}],
  "tool_requirements": {"needs_rag": bool, "needs_web_search": bool}
}
```

---

## References

- Paper: "MeetBench-XL: Calibrated Multi-Dimensional Evaluation and Learned Dual-Policy Agents for Real-Time Meetings" (arXiv:2602.03285)
- Repository: https://github.com/huyuelin/MeetBench-MeetAll.github.io
- Dataset: https://huggingface.co/datasets/YueLinHu/MeetAll-v2

---

*Last updated: June 2026*
