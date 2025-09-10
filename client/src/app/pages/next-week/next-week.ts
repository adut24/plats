import { Component } from '@angular/core';
import { AsyncPipe, NgClass } from '@angular/common';
import { getISOWeek } from 'date-fns';
import { ApiService, Recette } from '../../services/api';
import { Observable, forkJoin, map } from 'rxjs';
import { BADGE_COLOR } from '../../shared/badge-color';
import { Router } from '@angular/router';

@Component({
  selector: 'app-next-week',
  imports: [AsyncPipe, NgClass],
  templateUrl: './next-week.html',
  styleUrl: './next-week.scss'
})
export class NextWeek {
  private readonly recettes$: Observable<Recette[]>;
  private week_number: number;
  selectedRecettes = new Set<string>();
  hasPredefinedRecettes = false;

  constructor(private api: ApiService, private router: Router) {
    this.week_number = getISOWeek(new Date()) + 1;
    this.recettes$ = this.api.getRecettes().pipe(
      map((recettes: Recette[]) => {
        const build = this.buildRecettes(recettes)
        this.hasPredefinedRecettes = build.some(
          r => this.week_number === this.getWeekNumber(r.used)
        );
        return build;
      })
    );
  }

  get recettes(): Observable<Recette[]> {
    return this.recettes$;
  }

  private buildRecettes(all: Recette[]): Recette[] {
    let recettesSemaineProchaine = all.filter((recette) => this.week_number === this.getWeekNumber(recette.used));

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

  onCardClick(recette: Recette) {
    if (this.hasPredefinedRecettes) {
      this.router.navigate(['/recipe', recette.id]);
    } else {
      if (this.selectedRecettes.has(recette.id)) {
        this.selectedRecettes.delete(recette.id);
      } else {
        this.selectedRecettes.add(recette.id);
      }
    }
  }

  isSelected(recette: Recette): boolean {
    return this.selectedRecettes.has(recette.id);
  }

  canValidate(): boolean {
    return this.selectedRecettes.size >= 3 && this.selectedRecettes.size <= 4;
  }

  validateSelection() {
    if (!this.canValidate()) return;

    const requests = Array.from(this.selectedRecettes).map(id =>
      this.api.updateUsageTrue(id)
    );

    forkJoin(requests).subscribe({
      next: () => {
        window.location.reload();
      },
      error: (err) => {
        console.error('Erreur lors de la validation :', err);
      }
    });
  }
}
