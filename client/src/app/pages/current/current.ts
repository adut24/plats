import { Component } from '@angular/core';
import { ApiService, Recette } from '../../services/api';
import { getISOWeek } from 'date-fns';
import { Observable, map } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { BADGE_COLOR } from '../../shared/badge-color';

@Component({
  selector: 'app-current',
  imports: [AsyncPipe],
  templateUrl: './current.html',
  styleUrl: './current.scss'
})
export class Current {
  private readonly recettes$: Observable<Recette[]>;
  private week_number: number;

  constructor(private api: ApiService) {
    this.week_number = getISOWeek(new Date());
    this.recettes$ = this.api.getRecettes().pipe(
      map((recettes: Recette[]) => this.buildRecettes(recettes))
    );
  }

  get recettes(): Observable<Recette[]> {
    return this.recettes$;
  }

  private buildRecettes(all: Recette[]): Recette[] {
    return all.filter((recette) => this.week_number === this.getWeekNumber(recette.used));
  }

  getCategoryColor(cat: string): string {
    return BADGE_COLOR[cat] || '#ccc';
  }

  private getWeekNumber(date: Date | null): number {
    return date !== null ? getISOWeek(date) : -1;
  }
}
