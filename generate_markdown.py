def generate_markdown(entries: list[dict[str, any]]) -> None:
    md = ''
    for entry in entries:
        links = []
        if entry['paper'] is not None:
            links.append(f"[📄 Paper]({entry['paper']})")
        if entry['project_page'] is not None:
            links.append(f"[🌐 Project Page]({entry['project_page']})")
        if entry['code'] is not None:
            links.append(f"[💻 Code]({entry['code']})")
        if entry['video'] is not None:
            links.append(f"[🎥 Video]({entry['video']}'>video</a>)")
        link_string = ' | '.join(links)
        md_string = f"""
- <a name=\"{entry['id']}\"></a>
  **{entry['title']}**  
  {entry['authors']}  
  {entry['conference/journal']}, {entry['year']}  
  {link_string}  
  <details><summary>Abstract</summary>{entry['abstract']}</details>
"""
        md += md_string
    with open('README.md', 'w') as file:
        file.write(md)
