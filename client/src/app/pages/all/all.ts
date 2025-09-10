import { AsyncPipe } from '@angular/common';
import { Component } from '@angular/core';
import { Observable, map } from 'rxjs';
import { ApiService, Recette } from '../../services/api';
import { Router } from '@angular/router';
import { BADGE_COLOR } from '../../shared/badge-color';

@Component({
  selector: 'app-all',
  imports: [AsyncPipe],
  templateUrl: './all.html',
  styleUrl: './all.scss'
})
export class All {
  private readonly recettes$: Observable<Recette[]>;

  constructor(private api: ApiService, private router: Router) {
    this.recettes$ = this.api.getRecettes();
  }

  get recettes(): Observable<Recette[]> {
    return this.recettes$;
  }

  getCategoryColor(cat: string): string {
    return BADGE_COLOR[cat] || '#ccc';
  }

  onCardClick(recette: Recette) {
    this.router.navigate(['/recipe', recette.id]);
  }
}
