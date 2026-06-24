import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect(r'D:\AI_OS\00_dashboard\tasks.db')
conn.row_factory = sqlite3.Row

print('=== TASKS ===')
for r in conn.execute('SELECT id,title,status,priority,assigned_to,project FROM tasks WHERE status != "archived" ORDER BY priority,status'):
    title = r['title'].encode('ascii', 'replace').decode('ascii')
    print(f"[{r['id']}] P{r['priority']} | {r['status']:<12} | {r['assigned_to']:<22} | {r['project']:<16} | {title}")

print()
print('=== AGENTS ===')
for r in conn.execute('SELECT id,name,status,current_task_id FROM agents'):
    print(f"{r['id']:<25} | {r['status']:<8} | task:{r['current_task_id']}")

print()
print('=== ACTIVITY (last 10) ===')
for r in conn.execute('SELECT agent,action,created_at FROM activity ORDER BY id DESC LIMIT 10'):
    action = r['action'].encode('ascii', 'replace').decode('ascii')
    print(f"{r['created_at']} | {r['agent']:<20} | {action[:80]}")

conn.close()
