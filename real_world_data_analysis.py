# =============================================================================
# 🌍 Real-World Data Analysis Scenarios
# Daily Challenge | Data Analysis in Practice
# Understanding how data analysis drives real-world decisions
# =============================================================================

# =============================================================================
# 📚 WHAT YOU WILL LEARN
# =============================================================================
# - Understanding the practical applications of data analysis in real-world scenarios
# - Insight into how data analysis drives decision-making and problem-solving
# - Knowledge of various data analysis methodologies and their impacts

# =============================================================================
# 🎯 CHOSEN CASE STUDY
# Netflix: How Data Analysis Transformed a DVD Rental Company
# into the World's Largest Streaming Platform
#
# Industry:   Entertainment / Technology
# Type:       Business Case Study
# Relevance:  Ongoing (2006–present, with major 2024–2025 developments)
# Sources:    Netflix Research, McKinsey & Company, industry publications
# =============================================================================


def step_1_the_story():
    """
    STEP 1 — THE STORY
    ------------------
    Find and present a recent news story or business case study where
    data analysis played a crucial role.
    """
    story = """
    In the early 2000s, Netflix was a modest DVD-by-mail rental service competing
    against Blockbuster. Today it serves over 300 million subscribers across 190
    countries and generates billions of dollars in annual revenue. The transformation
    did not happen by accident — it was driven almost entirely by data analysis and
    algorithmic decision-making.

    The pivotal moment came in 2006, when Netflix launched the Netflix Prize — a public
    competition offering $1 million to any team that could improve their existing
    recommendation algorithm (called Cinematch) by at least 10%. This was a bold,
    public acknowledgment that their entire business strategy would be built around
    the science of understanding what people want to watch — before they know it themselves.

    The Prize attracted over 40,000 teams from across the world, generating enormous
    advances in machine learning and collaborative filtering. The winning team improved
    recommendation accuracy by 10.06%, and the lessons learned were integrated into
    what eventually became one of the most sophisticated data analysis systems ever
    built in the entertainment industry.

    By 2024, Netflix's recommendation engine analyses more than 250 content attributes
    per title — from cinematography style and soundtrack tempo to pacing and emotional
    tone. It processes over 1 million user events per second and personalises the
    experience for each of its 300+ million subscribers individually.
    """
    print("=" * 70)
    print("📰 STEP 1 — THE STORY")
    print("=" * 70)
    print(story)


def step_2_role_of_data_analysis():
    """
    STEP 2 — ROLE OF DATA ANALYSIS
    --------------------------------
    Analyze what data was analyzed, the methods used, and the outcomes.
    """

    # ── Data collected by Netflix ──────────────────────────────────────────
    data_categories = {
        "Viewing behaviour":  "What users watch, when they watch, and for how long",
        "Engagement signals": "Pause, rewind, fast-forward, and abandonment points",
        "Search patterns":    "What users search for but do not find or click",
        "Content attributes": "Genre, director, cast, pacing, mood, colour palette",
        "Device & context":   "What device is used, time of day, day of the week",
        "Thumbnail response": "Which artwork version users click on most",
        "Cultural factors":   "Regional preferences, local events, language settings",
    }

    # ── Methods and techniques used ────────────────────────────────────────
    methods = {
        "1. Collaborative Filtering": (
            "The foundation of the system. Identifies users with similar viewing "
            "histories and recommends content that users with matching tastes enjoyed. "
            "User-based: 'People like you also watched...' | "
            "Item-based: 'Because you watched X, you might like Y...'"
        ),
        "2. Content-Based Filtering": (
            "Each title is mapped against 250+ attributes. If a user consistently "
            "watches fast-paced thrillers, the system learns this pattern and filters "
            "content accordingly — even for titles with no user ratings yet."
        ),
        "3. Deep Learning & Neural Networks": (
            "Used to analyse video content directly — evaluating visual elements "
            "(colour, composition, camera movement) and audio features (soundtrack "
            "tempo, dialogue density), creating rich content profiles."
        ),
        "4. Matrix Factorization": (
            "A mathematical technique that decomposes the vast user-content interaction "
            "matrix into patterns, finding hidden relationships invisible to human analysts."
        ),
        "5. A/B Testing at Scale": (
            "Every change to the recommendation system is tested against a control group. "
            "Netflix runs hundreds of A/B tests simultaneously, analysing engagement, "
            "churn, and long-term satisfaction."
        ),
        "6. Contextual Bandits (Reinforcement Learning)": (
            "The system continuously learns in real time, adjusting recommendations "
            "based on what is working right now — not just historical patterns."
        ),
        "7. Thumbnail Personalisation": (
            "Netflix shows different thumbnail artwork of the same title to different "
            "users. In 2024, anime-style thumbnails boosted engagement by 35% in Japan. "
            "A Stranger Things thumbnail featuring a main character performed 23% better "
            "on mobile than one showing the show's monster."
        ),
    }

    print("=" * 70)
    print("🔍 STEP 2 — ROLE OF DATA ANALYSIS")
    print("=" * 70)

    print("\n📊 What Data Was Analysed:")
    print("-" * 40)
    for category, description in data_categories.items():
        print(f"  • {category}: {description}")

    print("\n🛠️  Methods and Techniques Used:")
    print("-" * 40)
    for method, description in methods.items():
        print(f"\n  {method}")
        print(f"    → {description}")

    print("\n📡 Scale of the Operation:")
    print("-" * 40)
    scale_facts = [
        "Serves over 300 million users globally",
        "Segments users into more than 1,000 unique taste groups",
        "Handles over 1 million events per second",
        "Analyses 250+ content attributes per title",
        "Reduces influence of older data by 20% each month",
    ]
    for fact in scale_facts:
        print(f"  • {fact}")


def step_3_impact_assessment():
    """
    STEP 3 — IMPACT ASSESSMENT
    ---------------------------
    How did data analysis impact the situation?
    What would have been different without it?
    """

    # ── Quantified impact ──────────────────────────────────────────────────
    impact_metrics = {
        "Content discovered via recommendations": "80%+ of all viewing (2024)",
        "Annual value of recommendation system":  "~$1 billion saved in churn",
        "User search time saved per day":         "Over 1,300 hours collectively",
        "Improvement from Netflix Prize":         "10.06% accuracy gain",
        "Customer satisfaction uplift":           "+20% (McKinsey)",
        "Conversion rate improvement":            "+10–15% (McKinsey)",
        "Thumbnail engagement uplift (Japan)":    "+35%",
    }

    # ── Problems solved by data analysis ──────────────────────────────────
    problems_solved = [
        (
            "The Discovery Problem",
            "Netflix's US catalogue has ~7,000 titles (2025). Users decide what to "
            "watch within 90 seconds — without recommendations, most would leave "
            "overwhelmed. Data analysis acts as the librarian for a massive library.",
        ),
        (
            "The Content Investment Problem",
            "House of Cards (2013) was commissioned based on data showing that fans "
            "of David Fincher's style also enjoyed political dramas and the original "
            "British series. Data reduced the risk of billion-dollar content decisions.",
        ),
        (
            "The Retention Problem",
            "Cultural personalisation and continuous recommendations prevent churn. "
            "This is estimated to save Netflix $1 billion annually.",
        ),
    ]

    print("\n" + "=" * 70)
    print("💡 STEP 3 — IMPACT ASSESSMENT")
    print("=" * 70)

    print("\n📈 Quantified Impact of Data Analysis:")
    print("-" * 40)
    for metric, result in impact_metrics.items():
        print(f"  • {metric}: {result}")

    print("\n🧩 Problems Solved by Data Analysis:")
    print("-" * 40)
    for i, (problem, solution) in enumerate(problems_solved, 1):
        print(f"\n  {i}. {problem}")
        print(f"     → {solution}")


def step_4_findings_and_significance():
    """
    STEP 4 — FINDINGS & SIGNIFICANCE
    ----------------------------------
    Present findings focused on the significance of data analysis
    in the context of the chosen story.
    """

    key_lessons = [
        (
            "Data analysis creates compounding value",
            "Every interaction makes the system smarter, creating a self-reinforcing "
            "cycle that competitors cannot easily replicate without the same depth "
            "of historical data.",
        ),
        (
            "Combination of methods matters more than any single technique",
            "Netflix blends collaborative filtering, content-based analysis, deep "
            "learning, and reinforcement learning. Complex real-world problems require "
            "multiple analytical perspectives applied together.",
        ),
        (
            "Data analysis enables decisions at impossible scale",
            "Personalising the experience for 300 million people simultaneously — "
            "with different thumbnails, row orders, and recommendations per person — "
            "is impossible without automated data analysis.",
        ),
        (
            "Measurement drives improvement",
            "Netflix's A/B testing culture ensures every insight is validated "
            "empirically. Hypothesis → test → measure → iterate separates genuine "
            "data analysis from storytelling with numbers.",
        ),
        (
            "The business case is measurable",
            "$1 billion in annual churn savings and 80%+ of viewing driven by "
            "recommendations provide a clear, quantifiable answer to why data "
            "analysis matters.",
        ),
    ]

    societal_implications = (
        "Netflix's model has influenced e-commerce (Amazon), music (Spotify), "
        "social media (TikTok's For You algorithm), and online education. "
        "However, personalisation also creates filter bubbles — users only see "
        "content confirming existing tastes. Responsible data analysis must balance "
        "optimisation for engagement with diversity, discovery, and user well-being."
    )

    print("\n" + "=" * 70)
    print("📝 STEP 4 — FINDINGS & SIGNIFICANCE")
    print("=" * 70)

    print("\n🔑 Key Lessons from the Netflix Case:")
    print("-" * 40)
    for i, (lesson, explanation) in enumerate(key_lessons, 1):
        print(f"\n  {i}. {lesson}")
        print(f"     → {explanation}")

    print("\n🌐 Broader Societal Implications:")
    print("-" * 40)
    print(f"  {societal_implications}")


def conclusion():
    """
    CONCLUSION
    ----------
    Summary of findings and key takeaways.
    """
    takeaways = [
        "Data analysis solves real problems — helping 300M people find content in 90 seconds",
        "Multiple analytical methods work better together than any single approach",
        "The impact of data analysis is measurable — $1B churn saving, 80%+ content discovery",
        "Data analysis scales decisions that no human team could make manually",
        "Ethical considerations (filter bubbles, data privacy) must be part of every strategy",
    ]

    sources = {
        "Netflix Research":          "https://research.netflix.com/research-area/recommendations",
        "arXiv (2025 study)":        "https://arxiv.org/html/2511.07280v1",
        "BrainForge AI":             "https://www.brainforge.ai/blog/how-netflix-uses-machine-learning-ml-to-create-perfect-recommendations",
        "Stratoflow":                "https://stratoflow.com/how-netflix-recommendation-system-works/",
        "LongStories.ai":            "https://longstories.ai/blog/how-netflix-predicts-what-you-watch",
        "AI & Data Analytics Network":"https://www.aidataanalytics.network/data-science-ai/articles/data-science-at-netflix-how-advanced-data-analytics-helped-netflix-generate-billions",
    }

    print("\n" + "=" * 70)
    print("✅ CONCLUSION")
    print("=" * 70)
    print("""
    Netflix's transformation from a DVD rental service into a global streaming
    giant is one of the most powerful real-world examples of data analysis
    driving business success. Its recommendation system — built on collaborative
    filtering, deep learning, A/B testing, and reinforcement learning —
    demonstrates that data analysis is not merely a technical function.
    It is a strategic capability that can redefine an entire industry.

    Without data analysis, Netflix would be a catalogue.
    With it, Netflix is a personalised experience — and that difference is worth billions.
    """)

    print("🔑 Key Takeaways:")
    print("-" * 40)
    for takeaway in takeaways:
        print(f"  • {takeaway}")

    print("\n📚 Sources:")
    print("-" * 40)
    for name, url in sources.items():
        print(f"  • {name}: {url}")

    print("\n" + "=" * 70)
    print("  Last Updated: January 2026")
    print("=" * 70)


# =============================================================================
# MAIN — Run all four steps
# =============================================================================
if __name__ == "__main__":
    step_1_the_story()
    step_2_role_of_data_analysis()
    step_3_impact_assessment()
    step_4_findings_and_significance()
    conclusion()
