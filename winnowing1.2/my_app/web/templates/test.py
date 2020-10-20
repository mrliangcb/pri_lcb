{ %
for duan in doc1_wrap %}
{{duan}}
{ %
for g_id, s, e in duan %}
{ % if g_id == -1 %}
{{doc1_str}}
{{doc1_str[duan][s:e + 1]}}
{ % else %}
< a
href = "#{{g_id}}"
name = "clickable" > {{doc1_str[s:e + 1]}} < / a >
{ % endif %}
< br >
{ % endfor %}

{ % endfor %}