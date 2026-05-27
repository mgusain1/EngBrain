

def chunk_file(content:str,max_lines:int=80,overlap:int=10):
    lines = content.splitlines()
    chunks = []
    start =0
    while start < len(lines):
        end = start + max_lines
        if end > len(lines):
            end = len(lines)
        now = lines[start:end]
        chunk_text = "\n".join(now).strip()
        if chunk_text is not None:
            chunks.append({
                "chunk_text":chunk_text,
                "start_line":start+1,
                "end_line":end
            })
        if end == len(lines):
            break
        start = end-overlap
    return chunks