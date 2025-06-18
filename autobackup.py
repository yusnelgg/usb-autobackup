import os
import sys
import shutil
import time
import json
from rich.console import Console

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

source = ''
target = ''

class MyHandler(FileSystemEventHandler):
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def on_modified(self, event):
        console.print(f"[green]✓ Modified:[/green] {event.src_path}")
        copy_changes(self.source, self.target)
    def on_created(self, event):
        console.print(f"[green]✓ Created:[/green] {event.src_path}")
        copy_changes(self.source, self.target)
    def on_deleted(self, event):
        console.print(f"[green]✗ Deleted:[/green] {event.src_path}")
        copy_changes(self.source, self.target)


console = Console()

def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading configuration:[/red] {e}")
        sys.exit(1)

def copy_changes(source, target, retries=10, delay=2):
    changes = 0
    for root, _, files in os.walk(source):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source)
            target_path = os.path.join(target, relative_path)

            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            if not os.path.exists(target_path) or os.path.getmtime(source_path) > os.path.getmtime(target_path):
                for attempt in range(retries):
                    try:
                        shutil.copy2(source_path, target_path)
                        console.print(f"[green]✓ Copied:[/green] {relative_path}")
                        changes += 1
                        break
                    except PermissionError as e:
                        if attempt < retries - 1:
                            time.sleep(delay)
                        else:
                            console.print(f"[red]✗ Error copying ({e}):[/red] {relative_path}")
    if changes == 0:
        console.print("[yellow]Nothing new to copy.[/yellow]")

def main():
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        config = load_config(sys.argv[1])
        backups = config.get("backups", [])
        if not backups:
            console.print("[red]No backup configurations found in the file.[/red]")
            sys.exit(1)
        observers = []
        console.print("[bold blue]Starting multiple backups... Press Ctrl+C to stop[/bold blue]\n")
        for backup in backups:
            src = backup.get("source")
            tgt = backup.get("target")
            if not src or not tgt:
                console.print("[red]Each backup must define 'source' and 'target'.[/red]")
                continue

            if not os.path.exists(src):
                console.print(f"[red]Error: Source folder {src} does not exist.[/red]")
                continue
            if not os.path.exists(tgt):
                console.print(f"[red]Error: Target folder {tgt} does not exist.[/red]")
                continue

            console.print(f"[bold blue]Backup:[/bold blue] Source: {src}  → Target: {tgt}")
            copy_changes(src, tgt)
            event_handler = MyHandler(src, tgt)
            observer = Observer()
            observer.schedule(event_handler, src, recursive=True)
            observer.start()
            observers.append(observer)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for obs in observers:
                obs.stop()
            console.print("\n[bold red]⛔ Backup stopped by user.[/bold red]")
            for obs in observers:
                obs.join()
        sys.exit(0)
    elif len(sys.argv) >= 3:
        source = sys.argv[1]
        target = sys.argv[2]

        if not os.path.exists(source):
            console.print(f"[red]Error:[/red] Source folder does not exist.")
            sys.exit(1)

        if not os.path.exists(target):
            console.print(f"[red]Error:[/red] Target folder does not exist.")
            sys.exit(1)

        console.print(f"[bold blue]📁 Source:[/bold blue] {source}")
        console.print(f"[bold blue]💾 Target:[/bold blue] {target}\n")
        console.print("Reporting changes to target")
        copy_changes(source, target)
        console.print(f"[bold green]🟢 Auto backup started... Press Ctrl+C to stop[/bold green]\n")
        event_handler = MyHandler(source, target)
        observer = Observer()
        observer.schedule(event_handler, source, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            console.print("\n[bold red]⛔ Backup stopped by user.[/bold red]")
        observer.join()
    else:
        console.print("[red]Usage:[/red] python autobackup.py /path/source /path/target")
        console.print("[red]   or:[/red] python autobackup.py config.json")
        sys.exit(1)

if __name__ == "__main__":
    main()
