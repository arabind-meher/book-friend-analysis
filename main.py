from nlp import ReviewSummarizer

# Example
if __name__ == "__main__":
    reviews = [
        "Loved the pacing and the character development. The ending was satisfying and tied up all major plot threads in a way that felt earned. I especially appreciated how the author handled the antagonist's arc, giving them depth rather than making them a one-dimensional villain.",
        "Great writing overall, but a few chapters dragged on with overly descriptive passages. While I enjoy detailed world-building, there were moments where the story’s momentum slowed. Still, the author’s command of dialogue kept me invested, and the relationships between characters were engaging and believable.",
        "Overhyped for me. Some plot holes in the central mystery left me unconvinced, and the prose felt uneven at times—beautiful in certain chapters but rushed and clumsy in others. I also felt the subplot involving the sidekick was left unresolved, which was disappointing.",
        "Audiobook narration was stellar; the narrator brought each character to life with distinct voices and subtle emotional inflections. This made the slower sections much easier to get through. I would recommend the audiobook format for anyone considering reading this title, as it elevates the experience.",
        "The thematic exploration of grief and recovery was heartfelt and moving, though occasionally heavy-handed. There were a few passages that felt more like lectures than natural parts of the story. That said, the emotional core of the book resonated with me, and I found myself thinking about certain scenes long after finishing.",
    ]

    summarizer = ReviewSummarizer(device=0)  # CPU
    print(ReviewSummarizer.clean_review(summarizer.summarize(reviews)))
