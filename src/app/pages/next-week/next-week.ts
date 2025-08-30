import { Component } from '@angular/core';
import { AsyncPipe } from '@angular/common';
import { getISOWeek } from 'date-fns';
import { ApiService, Recette } from '../../services/api';
import { Observable, map } from 'rxjs';
import { BADGE_COLOR } from '../../shared/badge-color';

@Component({
  selector: 'app-next-week',
  imports: [AsyncPipe],
  templateUrl: './next-week.html',
  styleUrl: './next-week.scss'
})
export class NextWeek {
  private readonly recettes$: Observable<Recette[]>;

  private week_number: number;

  constructor(private api: ApiService) {
    this.week_number = getISOWeek(new Date()) + 1;
    this.recettes$ = this.api.getRecettes().pipe(
      map((recettes: Recette[]) => this.buildRecettes(recettes))
    );
  }

  get recettes(): Observable<Recette[]> {
    return this.recettes$;
  }

  private buildRecettes(all: Recette[]): Recette[] {
    let recettesSemaineProchaine = all.filter((recette) => this.week_number === this.getWeekNumber(recette.used));
    return all;
    if (recettesSemaineProchaine.length !== 0) {
      return recettesSemaineProchaine;
    }

    recettesSemaineProchaine = all.filter((recette) => recette.used === null);
    const recettesParCategories = new Map<string, Recette[]>();
    for (const recette of recettesSemaineProchaine) {
      for (const categorie of recette.categories) {
        if (!recettesParCategories.has(categorie)) {
          recettesParCategories.set(categorie, []);
        }
        recettesParCategories.get(categorie)!.push(recette);
      }
    }

    const recettesAleatoires = new Set<Recette>();
    for (const recettes of recettesParCategories.values()) {
      const shuffled = [...recettes].sort(() => Math.random() - 0.5);
      recettesAleatoires.add(shuffled[0]);
      if (shuffled[1]) {
        recettesAleatoires.add(shuffled[1]);
      }
    }

    return [...recettesAleatoires].sort(() => Math.random() - 0.5).slice(0, 12);
  }

  getCategoryColor(cat: string): string {
    return BADGE_COLOR[cat] || '#ccc';
  }

  private getWeekNumber(date: Date | null): number {
    return date !== null ? getISOWeek(date) : -1;
  }
}
