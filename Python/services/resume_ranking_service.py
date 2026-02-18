from DS.priority_queue import PriorityQueue
from services.resume_score_service import calculate_resume_score
from services.resume_service import ResumeService

resume_service = ResumeService()

def rank_resumes(resumes, user_email):
    pq = PriorityQueue()

    for resume_meta in resumes:
        full_resume = resume_service.get_resume_by_id(
            resume_meta["_id"]
        )

        score, _, _ = calculate_resume_score(full_resume)

        resume_meta["score"] = score
        pq.push((score, resume_meta))

    ranked = []
    rank = 1

    while not pq.is_empty():
        score, resume = pq.pop()
        resume["rank"] = rank
        ranked.append(resume)
        rank += 1

    return ranked
