import os
import re
from collections import Counter
from datetime import datetime


# Change this value to process a different .txt file.
INPUT_FILE = os.path.join("text_samples", "technical_report_long.txt")


def choose_input_file(base_dir):
	"""Let the user choose a .txt file at runtime; fallback to INPUT_FILE."""
	default_path = os.path.join(base_dir, INPUT_FILE)
	samples_dir = os.path.join(base_dir, "text_samples")

	if not os.path.isdir(samples_dir):
		return default_path

	txt_files = sorted(
		name for name in os.listdir(samples_dir) if name.lower().endswith(".txt")
	)

	if not txt_files:
		return default_path

	print("Choose a .txt file to process:")
	for idx, name in enumerate(txt_files, start=1):
		print(f"{idx}. {name}")
	print(f"Press Enter for default: {os.path.basename(default_path)}")

	choice = input("Selection: ").strip()
	if not choice:
		return default_path

	if choice.isdigit():
		selection = int(choice)
		if 1 <= selection <= len(txt_files):
			return os.path.join(samples_dir, txt_files[selection - 1])

	custom_path = os.path.join(base_dir, choice)
	if os.path.isfile(custom_path) and custom_path.lower().endswith(".txt"):
		return custom_path

	print("Invalid selection. Using default file.")
	return default_path


def analyze_and_summarize(report_text):
	"""Analyze report text and return metadata plus a simulated AI summary."""
	words = report_text.split()
	lines = report_text.splitlines()

	word_count = len(words)
	line_count = len(lines)

	keyword_order = ["privacy", "encryption", "regulation"]
	lowered_text = report_text.lower()

	topic_tag = "GENERAL"
	found_keywords = []
	for keyword in keyword_order:
		if keyword in lowered_text:
			found_keywords.append(keyword)
			if topic_tag == "GENERAL":
				topic_tag = keyword.upper()

	if topic_tag == "GENERAL":
		tokens = re.findall(r"[a-zA-Z]{4,}", lowered_text)
		stopwords = {
			"this", "that", "with", "from", "have", "were", "been", "will",
			"into", "over", "then", "than", "also", "such", "their", "they",
			"them", "your", "you", "about", "across", "through", "using",
			"used", "when", "where", "while", "which", "what", "there",
			"would", "could", "should", "project", "report", "document",
			"system", "analysis", "summary", "overall", "based", "team",
			"campus", "pilot", "phase", "next", "data"
		}
		filtered = [token for token in tokens if token not in stopwords]
		common_terms = [term for term, _ in Counter(filtered).most_common(3)]
		if common_terms:
			found_keywords = common_terms
			topic_tag = common_terms[0].upper()

	long_warning = "[LONG DOCUMENT]" if word_count > 300 else ""

	keyword_text = ", ".join(found_keywords) if found_keywords else "none"
	summary = f"""{long_warning} This report is tagged as {topic_tag} and contains {word_count} words across {line_count} lines.
The system detected keywords: {keyword_text}.
Overall, the document presents technical or reflective insights suitable for quick AI-assisted review.""".strip()

	return {
		"topic_tag": topic_tag,
		"word_count": word_count,
		"line_count": line_count,
		"long_warning": long_warning,
		"summary": summary,
	}


if __name__ == "__main__":
	base_dir = os.path.dirname(os.path.abspath(__file__))
	input_path = choose_input_file(base_dir)
	log_path = os.path.join(base_dir, "summary_log.txt")

	try:
		with open(input_path, "r", encoding="utf-8") as file:
			report = file.read()

		analysis = analyze_and_summarize(report)

		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		log_entry = (
			"\n" + "=" * 60 + "\n"

			f"Timestamp: {timestamp}\n"
			f"Source File: {os.path.basename(input_path)}\n"
			f"Topic Tag: {analysis['topic_tag']}\n"
			f"Word Count: {analysis['word_count']}\n"
			f"Line Count: {analysis['line_count']}\n"
			f"Summary: {analysis['summary']}\n"
		)

		with open(log_path, "a", encoding="utf-8") as log_file:
			log_file.write(log_entry)

		print("Processing complete.")
		print(f"Input file: {input_path}")
		print(f"Topic tag: {analysis['topic_tag']}")
		print(f"Word count: {analysis['word_count']}")
		print(f"Line count: {analysis['line_count']}")
		print(f"AI summary: {analysis['summary']}")
		print(f"Log written to: {log_path}")
	except FileNotFoundError:
		print(f"Could not find file: {input_path}")
