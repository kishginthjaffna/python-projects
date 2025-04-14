from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


# Initialize the LLM
llm = ChatGroq(
    temperature=0,
    groq_api_key='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',
    model_name="llama3-70b-8192"
)

# Define the prompt template
full_prompt = PromptTemplate.from_template("""
            You are a smart and friendly assistant. The following is a chunk of transcript from a YouTube video. 
            Your task is to extract and clearly explain the key information, insights, or facts from it in a simple, easy-to-understand way. 
            Avoid just repeating what was said — instead, explain what the speaker is trying to teach or share.

            Transcript:
            {transcript}

            Explain the main points from this part in simple words:
            """)


# Get transcript from YouTube
def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry["text"] for entry in transcript])
        return full_text
    except NoTranscriptFound:
        return "Transcript not available for this video."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# I had to change the chunk size to 2000 tokens to fit comfortably under 6000 TPM (tokens per minute) for the summarization.
# This is because the LLM has a limit of 4096 tokens, and we want to ensure we stay well within that limit.
# Summarize using Groq
def chunk_text(text, max_tokens=2000):
    words = text.split()
    chunk_size = max_tokens  # adjust this value to fit comfortably under 6000 TPM
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def summarize_youtube_video(video_id):
    transcript = get_youtube_transcript(video_id)
    if transcript.startswith("Transcript not available") or transcript.startswith("An error occurred"):
        return transcript

    chunks = chunk_text(transcript, max_tokens=1500)
    partial_summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        prompt_input = full_prompt.format(transcript=chunk)
        summary = llm.invoke(prompt_input)
        partial_summaries.append(summary.content)

    # Final summary of all partial summaries
    final_prompt = PromptTemplate.from_template(
            """
            You are a helpful assistant. The following are simplified explanations of several parts of a YouTube video. 
            Combine them into one clear, short summary that explains the video’s key information and ideas in a way that anyone can easily understand.

            Partial Summaries:
            {partial_summaries}

            Final Summary:
            """)

    combined_summary_input = final_prompt.format(partial_summaries=" ".join(partial_summaries))
    final_summary = llm.invoke(combined_summary_input)

    return final_summary.content


# # Main function
# if __name__ == "__main__":
#     url = input("Enter YouTube video URL or ID: ")

#     # Extract video ID
#     if "watch?v=" in url:
#         video_id = url.split("watch?v=")[-1].split("&")[0]
#     else:
#         video_id = url.strip()

#     summary = summarize_youtube_video(video_id)
#     print("\nSummary:\n")
#     print(summary)
