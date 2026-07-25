def compute_hybrid_score(ats_score: int, matched_keywords: list, missing_keywords: list) -> dict:
    """
    Compute a hybrid ATS score by combining Gemini's ATS score with keyword coverage.
    
    Parameters:
        ats_score (int): Raw ATS score returned by Gemini (0-100).
        matched_keywords (list): Keywords found in resume.
        missing_keywords (list): Keywords missing from resume.
    
    Returns:
        dict: {
            "overall_score": int,
            "semantic_score": int,
            "keyword_score": int
        }
    """
    # Keyword coverage percentage
    total_keywords = len(matched_keywords) + len(missing_keywords)
    if total_keywords > 0:
        keyword_score = int((len(matched_keywords) / total_keywords) * 100)
    else:
        keyword_score = 0

    # Semantic score is Gemini’s ATS score
    semantic_score = ats_score

    # Hybrid overall score: weighted average
    # Example: 60% semantic, 40% keyword coverage
    overall_score = int((semantic_score * 0.6) + (keyword_score * 0.4))

    return {
        "overall_score": overall_score,
        "semantic_score": semantic_score,
        "keyword_score": keyword_score
    }
