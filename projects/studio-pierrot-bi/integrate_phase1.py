import re

# Read the source file (index.html) to get Phase 1 HTML content
with open('dashboard/index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract Phase 1 content (from KPI Cards to end of Data Table)
# Find the start: "<!-- KPI Cards -->"
# Find the end: "</div>" after the table
start_marker = '<!-- KPI Cards -->'
end_marker = '<!-- Data Table -->'

start_idx = index_content.find(start_marker)
# Find the closing div after the table section
table_section_start = index_content.find(end_marker)
# Find the end of the table card div
table_end = index_content.find('</div>\n\n  </main>', table_section_start)

if start_idx != -1 and table_end != -1:
    phase1_html = index_content[start_idx:table_end + len('</div>')]
    
    # Read multi-tab file
    with open('dashboard/index-multitab.html', 'r', encoding='utf-8') as f:
        multitab_content = f.read()
    
    # Find and replace the placeholder
    placeholder_start = multitab_content.find('<!-- Placeholder for Phase 1 content -->')
    if placeholder_start != -1:
        # Find the end of the placeholder div
        placeholder_end = multitab_content.find('</div>\n        </div>\n\n        <!-- Tab 2:', placeholder_start)
        
        if placeholder_end != -1:
            # Replace placeholder with actual Phase 1 content
            new_content = (multitab_content[:placeholder_start] + 
                          phase1_html + 
                          multitab_content[placeholder_end + len('</div>'):])
            
            # Write the updated file
            with open('dashboard/index-multitab.html', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Successfully integrated Phase 1 HTML content into multi-tab dashboard")
        else:
            print("❌ Could not find placeholder end")
    else:
        print("❌ Could not find placeholder start")
else:
    print(f"❌ Could not find Phase 1 content markers (start: {start_idx}, end: {table_end})")
