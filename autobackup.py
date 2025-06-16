import os
import sys
import shutil
import time
from rich.console import Console

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

source = ''
target = ''

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"Se ha modificado: {event.src_path}")
        copy_changes(source, target)
    def on_created(self, event):
        print(f"Se ha creado: {event.src_path}")
        # copy_changes(source, target)
    def on_deleted(self, event):
        print(f"Se ha borrado: {event.src_path}")
        copy_changes(source, target)


console = Console()

def copy_changes(source, target):
    changes = 0
    for root, _, files in os.walk(source):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source)
            target_path = os.path.join(target, relative_path)

            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            if not os.path.exists(target_path) or os.path.getmtime(source_path) > os.path.getmtime(target_path):
                shutil.copy2(source_path, target_path)
                console.print(f"[green]✓ Copied:[/green] {relative_path}")
                changes += 1

    if changes == 0:
        console.print("[yellow]Nothing new to copy.[/yellow]")

def main():
    
    if len(sys.argv) < 3:
        console.print("[red]Usage:[/red] python autobackup.py /source/path /target/path")
        sys.exit(1)
    
    global source, target

    source = sys.argv[1]
    target = sys.argv[2]

    if not os.path.exists(source):
        console.print(f"[red]Error:[/red] Source folder does not exist.")
        sys.exit(1)

    if not os.path.exists(target):
        console.print(f"[red]Error:[/red] Target folder does not exist.")
        sys.exit(1)

    console.print(f"[bold blue]📁 Source:[/bold blue] {source}")
    console.print(f"[bold blue]💾 Target:[/bold blue] {target}")
    
    console.print(f"Reporting changes to target")
    copy_changes(source, target)
    
    console.print(f"[bold green]🟢 Auto backup started... Press Ctrl+C to stop[/bold green]\n")
    
    try:
        
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, source, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    except KeyboardInterrupt:
        console.print("\n[bold red]⛔ Backup stopped by user.[/bold red]")

if __name__ == "__main__":
    main()
