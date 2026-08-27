import { Component, signal, inject, OnInit } from '@angular/core';
import { MangaTrackerAPIService } from './api/manga.service';
import type { Manga } from './api/model';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
  <h1>My Manga</h1>
  @if (loading()) {
    <p>Loading...</p>
  } @else {
    <ul>
      @for (manga of mangaList(); track manga.id) {
        <li>
          <strong>{{ manga.title }}</strong>
          - {{ manga.status }} (chapter {{ manga.chapters_read }})
        </li>
      } @empty {
        <li>No manga yet.</li>
      }
    </ul>
  }
  `,
})

export class App implements OnInit{
  private readonly api = inject(MangaTrackerAPIService);

  readonly mangaList = signal<Manga[]>([]);
  readonly loading = signal(true);

  ngOnInit(): void {
    this.api.listManga().subscribe((manga) => {
      this.mangaList.set(manga);
      this.loading.set(false);
    });
  }
}
