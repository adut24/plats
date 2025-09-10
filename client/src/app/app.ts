import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { differenceInWeeks } from 'date-fns';
import { ApiService, Recette } from './services/api';
import { Topbar } from './topbar/topbar';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Topbar],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnInit {
  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.cleanOldRecettes();
  }

  private cleanOldRecettes() {
    this.api.getRecettes().subscribe({
      next: (recettes: Recette[]) => {
        for (const recette of recettes) {
          if (recette.used && differenceInWeeks(new Date(), recette.used) > 4) {
            this.api.updateUsageFalse(recette.id);
          }
        }
      },
      error: (err) => console.error('Erreur récupération recettes', err)
    });
  }
}
