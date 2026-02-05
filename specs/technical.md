# Project Chimera – Technical Specification
Status: Frozen (v1.0 – Day 1 Submission)

> This document is the single source of truth for all technical contracts,
> schemas, and interfaces in Project Chimera.
> No implementation may diverge from this specification.

 
*Planner–Worker–Judge Agentic Infrastructure with OCC Governance*

```markdown
# specs/technical.md

## 1. Agent Task JSON Schema

Standardized contract for task propagation across the FastRender Swarm. All agents consume/produce this schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://project-chimera.ai/schemas/agent-task/v1",
  "title": "AgentTask",
  "type": "object",
  "required": [
    "task_id",
    "agent_role",
    "input_payload",
    "expected_output",
    "confidence_score",
    "trace_id"
  ],
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "Globally unique task identifier (RFC 4122)"
    },
    "agent_role": {
      "type": "string",
      "enum": ["planner", "worker", "judge"],
      "description": "Role executing this task within P-W-J triad"
    },
    "input_payload": {
      "type": "object",
      "description": "Task-specific input parameters (role-dependent structure)",
      "minProperties": 1
    },
"output_contract_ref": {
  "type": "string",
  "description": "Reference ID or URI of the schema used by Judge agents to validate task output"
}

    },
    "confidence_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Agent's self-assessed confidence in output correctness (0.0–1.0)"
    },
    "trace_id": {
      "type": "string",
      "format": "uuid",
      "description": "Distributed tracing identifier for causal chain reconstruction"
    }
  },
  "additionalProperties": false
}
```

---

Judge confidence scores are authoritative and override all upstream
confidence signals for Optimistic Concurrency Control and HITL decisions.



## 2. Judge Verdict Schema

Immutable verdict record produced by Judge agents after output validation. Triggers OCC resolution or HITL escalation.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://project-chimera.ai/schemas/judge-verdict/v1",
  "title": "JudgeVerdict",
  "type": "object",
  "required": [
    "verdict",
    "confidence_score",
    "reasoning",
    "requires_human_review"
  ],
  "properties": {
    "verdict": {
      "type": "string",
      "enum": ["APPROVE", "REJECT", "ESCALATE"],
      "description": "Atomic resolution decision per OCC protocol"
    },
    "confidence_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Judge's confidence in verdict correctness (0.0–1.0)"
    },
    "reasoning": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048,
      "description": "Structured rationale for verdict (machine-parseable fragments allowed)"
    },
    "requires_human_review": {
      "type": "boolean",
      "description": "Explicit flag triggering Human-in-the-Loop escalation path"
    }
  },
  "additionalProperties": false
}
```

---

## 3. Core Domain Objects

### 3.1 TrendSignal
*Represents detected socio-cultural signals from external data streams*

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://project-chimera.ai/schemas/trend-signal/v1",
  "title": "TrendSignal",
  "type": "object",
  "required": [
    "signal_id",
    "source_platforms",
    "topics",
    "signal_strength",
    "velocity",
    "detected_at"
  ],
  "properties": {
    "signal_id": {
      "type": "string",
      "format": "uuid"
    },
    "source_platforms": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["tiktok", "instagram", "twitter", "reddit", "youtube"]
      },
      "minItems": 1,
      "uniqueItems": true
    },
    "topics": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[a-z0-9-]{3,32}$"
      },
      "minItems": 1,
      "maxItems": 10
    },
    "signal_strength": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Normalized engagement intensity metric"
    },
    "velocity": {
      "type": "number",
      "minimum": 0.0,
      "description": "Rate of signal propagation (engagements/minute)"
    },
    "detected_at": {
      "type": "string",
      "format": "date-time"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true,
      "description": "Source-specific contextual attributes"
    }
  },
  "additionalProperties": false
}
```

### 3.2 ContentArtifact
*Immutable output produced by Worker agents after task execution*

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://project-chimera.ai/schemas/content-artifact/v1",
  "title": "ContentArtifact",
  "type": "object",
  "required": [
    "artifact_id",
    "content_type",
    "payload",
    "source_task_id",
    "created_at"
  ],
  "properties": {
    "artifact_id": {
      "type": "string",
      "format": "uuid"
    },
    "content_type": {
      "type": "string",
      "enum": [
        "short_video_script",
        "image_prompt",
        "caption_copy",
        "hashtag_set",
        "audio_script"
      ]
    },
    "payload": {
      "type": "object",
      "required": ["raw"],
      "properties": {
        "raw": {
          "type": "string",
          "minLength": 1
        },
        "structured": {
          "type": "object",
          "description": "Parsed representation (optional, type-dependent)"
        }
      }
    },
    "source_task_id": {
      "type": "string",
      "format": "uuid",
      "description": "Originating AgentTask.task_id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "provenance": {
      "type": "object",
      "properties": {
        "trend_signals": {
          "type": "array",
          "items": { "type": "string", "format": "uuid" }
        },
        "style_references": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "additionalProperties": false
}
```

### 3.3 HITLReviewRequest
*Escalation payload for human reviewers when OCC fails or confidence thresholds breached*

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://project-chimera.ai/schemas/hitl-review-request/v1",
  "title": "HITLReviewRequest",
  "type": "object",
  "required": [
    "request_id",
    "artifact_ref",
    "priority",
    "context_snapshot",
    "requested_action",
    "escalated_at"
  ],
  "properties": {
    "request_id": {
      "type": "string",
      "format": "uuid"
    },
    "artifact_ref": {
      "type": "string",
      "format": "uuid",
      "description": "ContentArtifact.artifact_id requiring review"
    },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "description": "1=lowest urgency, 5=critical path blocker"
    },
    "context_snapshot": {
      "type": "object",
      "required": ["task_chain", "judge_verdicts"],
      "properties": {
        "task_chain": {
          "type": "array",
          "items": { "type": "string", "format": "uuid" },
          "description": "Chronological task_id sequence"
        },
        "judge_verdicts": {
          "type": "array",
          "items": { "$ref": "https://project-chimera.ai/schemas/judge-verdict/v1" }
        }
      }
    },
    "requested_action": {
      "type": "string",
      "enum": [
        "approve_with_modifications",
        "reject_and_regenerate",
        "approve_as_is",
        "request_additional_context"
      ]
    },
    "escalated_at": {
      "type": "string",
      "format": "date-time"
    }
  },
  "additionalProperties": false
}
```

---

## 4. MCP Tool Interface Definitions

*Model Context Protocol tool contracts for external system integration. All tools implement idempotent operations with explicit side-effect declarations.*

### 4.1 social_media_analytics
*Fetch real-time trend signals from platform APIs*

```json
{
  "tool_name": "social_media_analytics",
  "input_schema": {
    "type": "object",
    "required": ["platforms", "time_window_minutes", "min_engagement_threshold"],
    "properties": {
      "platforms": {
        "type": "array",
        "items": { "type": "string" },
        "minItems": 1
      },
      "time_window_minutes": {
        "type": "integer",
        "minimum": 5,
        "maximum": 1440
      },
      "min_engagement_threshold": {
        "type": "integer",
        "minimum": 10
      },
      "topic_filters": {
        "type": "array",
        "items": { "type": "string" },
        "maxItems": 20
      }
    }
  },
  "output_schema": {
    "type": "object",
    "required": ["signals", "query_timestamp"],
    "properties": {
      "signals": {
        "type": "array",
        "items": { "$ref": "https://project-chimera.ai/schemas/trend-signal/v1" }
      },
      "query_timestamp": {
        "type": "string",
        "format": "date-time"
      },
      "rate_limit_remaining": {
        "type": "integer",
        "minimum": 0
      }
    }
  },
  "side_effect_description": "Read-only analytics query. No state mutation. Subject to third-party API rate limits."
}
```

### 4.2 content_generator
*Produce ContentArtifact from structured prompts using generative models*

```json
{
  "tool_name": "content_generator",
  "input_schema": {
    "type": "object",
    "required": ["content_type", "prompt_template", "style_constraints"],
    "properties": {
      "content_type": {
        "type": "string",
        "enum": [
          "short_video_script",
          "image_prompt",
          "caption_copy",
          "hashtag_set",
          "audio_script"
        ]
      },
      "prompt_template": {
        "type": "string",
        "minLength": 10,
        "maxLength": 2000
      },
      "style_constraints": {
        "type": "object",
        "properties": {
          "tone": { "type": "string" },
          "max_length_tokens": { "type": "integer", "minimum": 10 },
          "brand_safety_level": {
            "type": "string",
            "enum": ["strict", "moderate", "lenient"]
          }
        }
      },
      "reference_artifacts": {
        "type": "array",
        "items": { "type": "string", "format": "uuid" },
        "maxItems": 5
      }
    }
  },
  "output_schema": {
    "type": "object",
    "required": ["artifact"],
    "properties": {
      "artifact": {
        "$ref": "https://project-chimera.ai/schemas/content-artifact/v1"
      },
      "generation_metadata": {
        "type": "object",
        "properties": {
          "model_version": { "type": "string" },
          "token_usage": {
            "type": "object",
            "properties": {
              "prompt_tokens": { "type": "integer" },
              "completion_tokens": { "type": "integer" }
            }
          }
        }
      }
    }
  },
  "side_effect_description": "Stateless generation. No persistent storage. Output must be persisted externally via separate artifact_store tool."
}
```

### 4.3 publishing_gateway
*OCC-governed content publication with optimistic concurrency checks*

```json
{
  "tool_name": "publishing_gateway",
  "input_schema": {
    "type": "object",
    "required": ["artifact_id", "target_platforms", "version_token"],
    "properties": {
      "artifact_id": {
        "type": "string",
        "format": "uuid"
      },
      "target_platforms": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["tiktok", "instagram", "twitter"]
        },
        "minItems": 1,
        "maxItems": 3
      },
      "version_token": {
        "type": "string",
        "description": "OCC version stamp from last known state (prevents overwrite conflicts)",
        "pattern": "^[a-f0-9]{64}$"
      },
      "schedule_utc": {
        "type": "string",
        "format": "date-time",
        "description": "Optional scheduled publish time (immediate if omitted)"
      }
    }
  },
  "output_schema": {
    "type": "object",
    "required": ["publication_id", "status", "version_token"],
    "properties": {
      "publication_id": {
        "type": "string",
        "format": "uuid"
      },
      "status": {
        "type": "string",
        "enum": ["published", "scheduled", "version_conflict", "platform_rejected"]
      },
      "version_token": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$",
        "description": "New version token if published/scheduled; unchanged on conflict"
      },
      "platform_responses": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["platform", "status_code"],
          "properties": {
            "platform": { "type": "string" },
            "status_code": { "type": "integer" },
            "external_id": { "type": "string" }
          }
        }
      }
    }
  },
  "side_effect_description": "MUTATING OPERATION: Publishes content to external platforms. OCC version_token prevents concurrent modification conflicts. Idempotent on version_conflict response."
}
```

### 4.4 artifact_store
*Immutable content artifact persistence with cryptographic integrity*

```json
{
  "tool_name": "artifact_store",
  "input_schema": {
    "type": "object",
    "required": ["artifact"],
    "properties": {
      "artifact": {
        "$ref": "https://project-chimera.ai/schemas/content-artifact/v1"
      }
    }
  },
  "output_schema": {
    "type": "object",
    "required": ["storage_key", "content_hash", "stored_at"],
    "properties": {
      "storage_key": {
        "type": "string",
        "pattern": "^artifact/[a-f0-9]{64}$"
      },
      "content_hash": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$",
        "description": "SHA-256 hash of canonicalized artifact JSON"
      },
      "stored_at": {
        "type": "string",
        "format": "date-time"
      }
    }
  },
  "side_effect_description": "MUTATING OPERATION: Writes immutable artifact to durable storage. Duplicate writes (same content_hash) return existing storage_key without error. No deletion permitted."
}
```

---

## Validation Compliance Notes

- All schemas conform to JSON Schema Draft 2020-12
- Pydantic v2+ compatible via `pydantic.json_schema.model_json_schema()`
- UUID formats assume RFC 4122 canonical representation
- Date-time formats assume RFC 3339 / ISO 8601 UTC representation
- No circular references or implementation-specific extensions
- All `$ref` URIs resolvable via local schema registry at runtime
```
*Document generated for Project Chimera v1.2 — Governance Layer Specification*



### HumanReviewDecision

Represents the final, authoritative decision made by a human moderator
after escalation by a Judge agent.

Fields:
- decision (approve | reject | modify)
- reviewer_id
- comments
- decided_at


