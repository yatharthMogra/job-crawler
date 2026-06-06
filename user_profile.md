# Candidate Profile Schema V1

```yaml
candidate_profile:

  schema_version:
    description: >
      Version identifier for the candidate profile schema.
      Used to support future migrations and compatibility handling.

    type: string

    example: "v1"

  timestamps:
    description: >
      Operational metadata used for synchronization, profile refreshes,
      debugging, and future reprocessing workflows.

    fields:

      profile_created_at:
        description: >
          Timestamp when the candidate profile was initially created.

        type: datetime

      profile_last_updated:
        description: >
          Timestamp of the latest profile modification.

        type: datetime

      resume_last_parsed_at:
        description: >
          Timestamp of the latest resume parsing operation.

        type: datetime

      capabilities_generated_at:
        description: >
          Timestamp when inferred capabilities were last generated.

        type: datetime

  identity:
    description: >
      Basic administrative and educational information about the candidate.
      Used for personalization and contextual matching.

    fields:

      candidate_id:
        description: >
          Internal unique identifier for the candidate.

        type: string

      name:
        description: >
          Candidate full name.

        type: string

      email:
        description: >
          Primary email address used for notifications and login.

        type: string

      education:
        description: >
          Current or most recent educational qualification.

        fields:

          degree:
            description: >
              Degree currently being pursued or completed.

            examples:
              - "MS Computer Science"
              - "B.Tech Data Science"

          university:
            description: >
              Educational institution name.

            examples:
              - "NYU"
              - "IIT Mandi"

          graduation_date:
            description: >
              Expected or completed graduation date.

            type: string

            example: "2027-05"

  constraints:
    description: >
      Hard filters that eliminate incompatible jobs before ranking begins.

    fields:

      sponsorship_required:
        description: >
          Whether the candidate requires employer sponsorship.

        type: boolean

      visa_type:
        description: >
          Candidate visa category.

        examples:
          - "F1"
          - "OPT"
          - "H1B"

      work_authorization:
        description: >
          Current work authorization status.

        examples:
          - "CPT_OPT"
          - "US_CITIZEN"
          - "GREEN_CARD"

      internship_only:
        description: >
          If true, only internship roles should be considered.

        type: boolean

      fulltime_only:
        description: >
          If true, only full-time roles should be considered.

        type: boolean

      minimum_salary:
        description: >
          Minimum acceptable annual salary.

        type: integer

        example: 120000

      minimum_hourly_rate:
        description: >
          Minimum acceptable hourly compensation.

        type: integer

        example: 25

  preferences:
    description: >
      Soft preferences used during ranking.
      Jobs violating these are not eliminated but ranked lower.

    fields:

      primary_roles:
        description: >
          Roles the candidate is actively prioritizing.

        examples:
          - "Software Engineer Intern"
          - "AI Engineer Intern"

      secondary_roles:
        description: >
          Roles acceptable to the candidate but lower priority.

        examples:
          - "Data Scientist Intern"
          - "ML Engineer Intern"

      preferred_locations:
        description: >
          Locations strongly preferred by the candidate.

        examples:
          - "NYC"
          - "Remote"

      acceptable_locations:
        description: >
          Locations acceptable but less preferred.

        examples:
          - "New Jersey"
          - "Connecticut"

      remote_preference:
        description: >
          Preferred work mode.

        examples:
          - "Remote"
          - "Hybrid"
          - "Onsite"

      relocation_allowed:
        description: >
          Whether candidate is willing to relocate.

        type: boolean

      preferred_company_stages:
        description: >
          Preferred company maturity categories.

        examples:
          - "Startup"
          - "Growth Stage"
          - "Enterprise"

      preferred_industries:
        description: >
          Industries the candidate prefers.

        examples:
          - "AI"
          - "FinTech"
          - "Developer Tools"

  evidence:
    description: >
      Structured source-of-truth information extracted from resume
      and user edits. Skills and capabilities are derived from this.

    fields:

      experiences:
        description: >
          Professional work experiences.

        object_structure:

          title:
            description: >
              Job title held by candidate.

            examples:
              - "Software Developer 2"

          company:
            description: >
              Organization name.

            examples:
              - "Walmart"

          duration_months:
            description: >
              Total duration of experience in months.

            type: integer

            example: 24

          domains:
            description: >
              Industry or business domains worked in.

            examples:
              - "Retail Tech"
              - "Healthcare AI"

          evidence_keywords:
            description: >
              Structured and normalized keywords extracted from
              experience bullets. Used for capability generation,
              recommendation matching, and explanation.

            examples:
              - "Backend APIs"
              - "Distributed Systems"
              - "Monitoring"
              - "Java"

      projects:
        description: >
          Personal, academic, startup, hackathon, or research projects.

        object_structure:

          name:
            description: >
              Project name.

            examples:
              - "SpecterRossAI"

          category:
            description: >
              Project type or classification.

            examples:
              - "AI Product"
              - "Research Project"
              - "Hackathon"

          domains:
            description: >
              Industry or technical domains relevant to project.

            examples:
              - "Legal Tech"
              - "Document Intelligence"

          evidence_keywords:
            description: >
              Structured and normalized technical and architectural
              signals extracted from project descriptions.

            examples:
              - "Multi-Agent Systems"
              - "React"
              - "Voice AI"
              - "RAG"
              - "Real-Time Systems"

      certifications:
        description: >
          Professional certifications or credentials.

        object_structure:

          name:
            description: >
              Certification title.

            examples:
              - "AWS Solutions Architect"

          issuer:
            description: >
              Organization issuing certification.

            examples:
              - "AWS"

  skills:
    description: >
      Explicit technical skills directly supported by evidence.

    fields:

      languages:
        description: >
          Programming languages known by candidate.

        examples:
          - "Python"
          - "Java"
          - "TypeScript"

      frameworks:
        description: >
          Frameworks and backend/frontend libraries.

        examples:
          - "React"
          - "FastAPI"
          - "Spring Boot"

      databases:
        description: >
          Database technologies used.

        examples:
          - "PostgreSQL"
          - "MongoDB"

      cloud:
        description: >
          Cloud platforms and services.

        examples:
          - "AWS"
          - "GCP"

      ai_ml:
        description: >
          AI/ML systems, workflows, and technologies.

        examples:
          - "RAG"
          - "LLMs"
          - "Multi-Agent Systems"

      infrastructure:
        description: >
          Infrastructure and platform engineering technologies.

        examples:
          - "Docker"
          - "Kafka"
          - "CI/CD"

      product:
        description: >
          Product engineering and builder-oriented traits.

        examples:
          - "Rapid Prototyping"
          - "Hackathons"
          - "AI-Assisted Development"

  capabilities:
    description: >
      High-level inferred engineering capabilities generated from evidence.
      Recommendation engine primarily matches using capabilities rather than raw keywords.

    object_structure:

      name:
        description: >
          Standardized capability selected from controlled taxonomy.

        examples:
          - "Backend Engineering"
          - "AI Systems"
          - "Distributed Systems"

      evidence:
        description: >
          Supporting evidence explaining why this capability exists.

        examples:
          - "Walmart"
          - "Backend APIs"
          - "Distributed Systems"
          - "SpecterRossAI"
          - "RAG Systems"

  capability_taxonomy_version:
    description: >
      Version identifier for capability taxonomy.
      Ensures consistency across profiles and recommendation systems.

    type: string

    example: "v1"

capability_taxonomy:

  - Backend Engineering

  - Frontend Engineering

  - Full Stack Development

  - AI Systems

  - Machine Learning

  - Machine Learning Research

  - Data Engineering

  - Distributed Systems

  - Cloud Infrastructure

  - Platform Engineering

  - DevOps

  - Product Engineering

  - Mobile Development

  - Security Engineering

  - Analytics Engineering

  - Research
```
