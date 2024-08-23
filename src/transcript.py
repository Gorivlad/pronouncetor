def save_transcript_to_txt(result, output_file):
    with open(output_file, 'w') as file:
        file.write("Full Transcription:\n")
        file.write(result['text'] + '\n\n')
        # Write each segment in a readable form
        for segment in result['segments']:
            file.write(f"Segment {segment['id']}:\n")
            file.write(f"Start: {segment['start']:.2f}s, End:"
                       f" {segment['end']:.2f}s\n")
            file.write(segment['text'] + '\n\n')
            # For timestamps of the words uncommed lines bellow
            # for word in segment['words']:
            #     file.write(
            #         f"  {word['word']} (Start: {word['start']:.2f}s, "
            #         f"End: {word['end']:.2f}s, Probability: "
            #         f"{word['probability']:.4f})\n")
            file.write('\n\n')


def filter_transcript(result):
    # Returns a formatted string
    lines = []
    lines.append("Full Transcription:\n")
    lines.append(result['text'] + '\n')
    # Write each segment in a readable form
    for segment in result['segments']:
        lines.append(f"Segment {segment['id']}:\n")
        lines.append(f"Start: {segment['start']:.2f}s, "
                     "End: {segment['end']:.2f}s\n")
        lines.append(segment['text'] + '\n')
        # For timestamps of words uncomment lines bellow
        # for word in segment['words']:
        #     lines.append(
        #         f"  {word['word']} (Start: {word['start']:.2f}s,"
        #         f" End: {word['end']:.2f}s, "
        #         f"Probability: {word['probability']:.4f})\n")
        lines.append('\n')

    return '\n'.join(lines)
