# SRS Diagrams for Resume Maker PPT

Ten diagrams for your Software Requirements Specification and PowerPoint. Each diagram is compact and fits on one slide. Use the instructions at the bottom to export as images.

---

## 1. Use Case Diagram

Clean, compact version for PPT: grouped use cases with fewer nodes and clearer labels.

```mermaid
flowchart LR
  User((User))
  Admin((Admin))

  subgraph system [Resume Maker System]
    direction LR

    subgraph userCases [User Use Cases]
      U1[Register and Login]
      U2[Reset Password]
      U3[Build Resume]
      U4[Generate Resume with AI]
      U5[Manage My Resumes]
      U6[Check ATS and Score]
      U7[Download PDF]
      U8[Submit Feedback]
    end

    subgraph adminCases [Admin Use Cases]
      A1[Admin Login]
      A2[Manage Users]
      A3[View Resume Analytics]
      A4[Export Reports and Logs]
    end
  end

  User --> U1
  User --> U2
  User --> U3
  User --> U4
  User --> U5
  User --> U6
  User --> U7
  User --> U8

  Admin --> A1
  Admin --> A2
  Admin --> A3
  Admin --> A4
```

**Tip:** In Mermaid Live, use a large zoom (e.g. 150–200%) or export as **SVG** for sharp text in PPT. If using PNG, choose the highest scale for a clear look.

---

## 2. Activity Diagram

Flow of activities for creating a resume manually: from template choice through steps to save. Decisions show success/failure and optional return to edit.

```mermaid
flowchart TD
  Start([Start]) --> ChooseTemplate[Choose Template]
  ChooseTemplate --> Step1[Step 1: Personal Info]
  Step1 --> Step2[Step 2: Education]
  Step2 --> Step3[Step 3: Experience]
  Step3 --> Step4[Step 4: Skills and Custom]
  Step4 --> Finish[Click Finish]
  Finish --> BuildPayload[Build payload from localStorage]
  BuildPayload --> Post[POST /api/resumes]
  Post --> Success{Success?}
  Success -->|Yes| Redirect[Redirect to Documents]
  Redirect --> End([End])
  Success -->|No| Error[Show error message]
  Error --> Step4
```

---

## 3. Sequence Diagram

Interaction flow for manual resume creation from UI steps to backend save and final redirect.

```mermaid
sequenceDiagram
  actor User
  participant UI as Frontend (Step Pages)
  participant LS as localStorage
  participant API as Flask API (/api/resumes)
  participant Service as ResumeService
  participant Repo as ResumeRepo
  participant DB as MongoDB

  User->>UI: Choose template
  UI->>LS: Save selectedTemplate
  loop Step 1 to Step 4
    User->>UI: Fill form step
    UI->>LS: Save step data
  end
  User->>UI: Click Finish
  UI->>LS: Read all step data
  UI->>API: POST /api/resumes (payload)
  API->>Service: create_resume(email, data)
  Service->>Repo: create_resume(document)
  Repo->>DB: insert_one(document)
  DB-->>Repo: inserted_id
  Repo-->>Service: success
  Service-->>API: success response
  API-->>UI: 201 Created
  UI-->>User: Redirect to documents.html
```

---

## 4. Class Diagram

Core backend class/module structure for authentication, resume operations, AI generation, and ATS analysis.

```mermaid
classDiagram
  class App {
    +create_app()
  }

  class UserController {
    +signup()
    +login()
    +get_profile()
    +update_profile()
  }

  class ResumeController {
    +create_resume()
    +get_resumes()
    +get_single_resume()
    +get_resume_score()
    +delete_resume()
  }

  class AIResumeController {
    +suggest_resume_from_role()
    +create_resume_with_ai()
  }

  class ATSController {
    +check_resume()
    +check_resume_from_saved()
  }

  class UserService {
    +signup_user()
    +login_user()
    +login_with_google()
  }

  class ResumeService {
    +create_resume(email, data)
    +get_user_resumes(email)
    +get_resume_by_id(id)
    +delete_resume(email, id)
  }

  class AIResumeService {
    +create_ai_resume(email, payload)
  }

  class ATSCheckerService {
    +check_resume(file, jobDescription)
    +check_resume_from_data(data, jobDescription)
  }

  class UserRepo {
    +create_user()
    +find_by_email()
    +update_user()
  }

  class ResumeRepo {
    +create_resume()
    +find_by_user()
    +find_by_id()
    +delete_by_id()
  }

  class ResumeGenerator {
    +suggest_from_role(role)
    +generate_resume(payload)
  }

  class MongoDB {
    users
    resumes
    feedbacks
  }

  App --> UserController
  App --> ResumeController
  App --> AIResumeController
  App --> ATSController

  UserController --> UserService
  ResumeController --> ResumeService
  AIResumeController --> AIResumeService
  ATSController --> ATSCheckerService

  UserService --> UserRepo
  ResumeService --> ResumeRepo
  AIResumeService --> ResumeGenerator
  AIResumeService --> ResumeRepo

  UserRepo --> MongoDB
  ResumeRepo --> MongoDB
```

---

## 5. System Architecture (High-Level)

Shows: Browser (FSD static), Flask app (Controllers → Services → Repos), MongoDB/Redis, Admin (Streamlit), and external services (Google OAuth, OpenAI).

```mermaid
flowchart LR
  subgraph client [Client]
    Browser["Browser\n(FSD HTML/CSS/JS)"]
  end
  subgraph backend [Flask App]
    Controllers[Controllers]
    Services[Services]
    Repos[Repos]
    Controllers --> Services --> Repos
  end
  subgraph data [Data]
    MongoDB[(MongoDB\nusers, resumes, feedbacks)]
    Redis[(Redis\ncache/session)]
  end
  subgraph admin [Admin]
    Streamlit[Streamlit\nAdmin Dashboard]
  end
  subgraph external [External]
    Google[Google OAuth]
    OpenAI[OpenAI API]
  end
  Browser <--> Controllers
  Repos --> MongoDB
  Repos --> Redis
  Streamlit -->|"/api/admin/*"| Controllers
  Controllers --> Google
  Controllers --> OpenAI
```

---

## 6. User Flow

End-to-end user journey: Landing → Auth → Dashboard → Create New, Create with AI, or Open/Score/ATS/Download.

```mermaid
flowchart TD
  Start([Landing Page]) --> Auth{Authenticate}
  Auth -->|Login/Signup/Google| Dashboard[Dashboard / Documents]
  Dashboard --> Path1[Create New Resume]
  Dashboard --> Path2[Create with AI]
  Dashboard --> Path3[Open / Score / ATS / Download]
  Path1 --> ChooseTemplate[Choose Template]
  ChooseTemplate --> Steps[Step 1 Personal → Step 2 Education\n→ Step 3 Experience → Step 4 Skills]
  Steps --> Finish[Finish - POST /api/resumes]
  Finish --> Dashboard
  Path2 --> AIModal[AI Form - Role, Details]
  AIModal --> AIPost[POST /ai/create-resume]
  AIPost --> Dashboard
  Path3 --> Preview[Preview Resume]
  Preview --> Score[Score / ATS Check / PDF Download]
  Auth -->|Forgot/Reset| Forgot[Forgot / Reset Password]
  Forgot --> Auth
```

---

## 7. Resume Creation Process (Step-by-Step)

Linear flow for "Create New Resume": template selection through save.

```mermaid
flowchart LR
  A[Choose Template\nchoose-template.html] --> B[Step 1\nPersonal Info]
  B --> C[Step 2\nEducation]
  C --> D[Step 3\nExperience]
  D --> E[Step 4\nSkills and Custom]
  E --> F[Finish\nPOST /api/resumes]
  F --> G[Documents\nList]
  subgraph client [Client - localStorage]
    B
    C
    D
    E
  end
```

---

## 8. 4.5 Data Flow Diagram

### 4.5.1 Level-0 DFD

Context-level view: external actors interact with one main process.

```mermaid
flowchart LR
  User[User]
  Admin[Admin]
  P0((P0: Resume Maker System))
  D1[(Users Data Store)]
  D2[(Resumes Data Store)]
  D3[(Feedback Data Store)]

  User -->|Signup/Login, Resume Input, ATS Request| P0
  P0 -->|Auth Status, Resume Output, Scores| User

  Admin -->|Admin Login, Manage/Analytics Requests| P0
  P0 -->|Reports, User/Resume Data| Admin

  P0 <--> D1
  P0 <--> D2
  P0 <--> D3
```

### 4.5.2 Level-1 DFD

Decomposition of P0 into major processes.

```mermaid
flowchart LR
  User[User]
  Admin[Admin]

  P1((P1: Authentication))
  P2((P2: Resume Builder))
  P3((P3: AI Resume Generator))
  P4((P4: ATS Checker))
  P5((P5: Admin Analytics))
  P6((P6: Feedback and Contact))

  D1[(D1 Users)]
  D2[(D2 Resumes)]
  D3[(D3 Feedbacks)]

  User --> P1
  P1 --> User
  P1 <--> D1

  User --> P2
  P2 --> User
  P2 <--> D2

  User --> P3
  P3 --> User
  P3 <--> D2

  User --> P4
  P4 --> User
  P4 <--> D2

  User --> P6
  P6 --> User
  P6 <--> D3

  Admin --> P5
  P5 --> Admin
  P5 <--> D1
  P5 <--> D2
```

### 4.5.3 Level-2 DFD

Detailed decomposition of **P2: Resume Builder**.

```mermaid
flowchart TD
  User[User]
  D2[(D2 Resumes)]

  P21((P2.1 Select Template))
  P22((P2.2 Enter Personal/Education/Experience/Skills))
  P23((P2.3 Validate and Build Payload))
  P24((P2.4 Save Resume))
  P25((P2.5 Retrieve and Preview Resume))
  P26((P2.6 Score/ATS/Download Output))

  User -->|Choose template| P21
  P21 --> P22
  User -->|Fill step forms| P22
  P22 --> P23
  P23 -->|POST /api/resumes| P24
  P24 --> D2
  D2 --> P25
  P25 -->|Preview data| User
  User -->|Score/ATS/Download request| P26
  P26 --> D2
  P26 -->|Score, ATS result, PDF output| User
```

---

## How to Use in PPT

- **Option A:** Paste each Mermaid code block into [Mermaid Live Editor](https://mermaid.live), then use **Download PNG** or **Download SVG**. Insert the image into a slide (one diagram per slide).
- **Option B:** In VS Code or Cursor, install a Mermaid extension (e.g. "Mermaid Preview"), open this file, preview, and export as image.
- **Option C:** For Word or Google Docs SRS, export each diagram as PNG from Mermaid Live and insert as picture.

One diagram per slide keeps text and boxes readable in your presentation.
