import { Component, OnInit } from '@angular/core';
import { ApiService, Recette } from '../../services/api';
import { getISOWeek } from 'date-fns';

@Component({
  selector: 'app-current',
  imports: [],
  templateUrl: './current.html',
  styleUrl: './current.scss'
})
export class Current implements OnInit {
  private _recettes: Recette[] = [];
  private colors: Record<string, string> = {
    'Burger': '#FF6B6B',
    'Bœuf': '#D9534F',
    'Frites': '#FFD93D',
    'Poulet': '#FFB347',
    'Fromage': '#FFD700',
    'Curry': '#FF8C00',
    'Patate Douce': '#FF7F50',
    'Riz': '#F0E68C',
    'Végétarien': '#8BC34A',
    'Porc': '#E9967A',
    'Panko': '#FFE4B5',
    'Chorizo': '#FF4500',
    'Dinde': '#F5DEB3',
    'Nouilles': '#F5DEB3',
    'Gnocchi': '#FFE4C4',
    'Champignons': '#A0522D',
    'Naan': '#F5F5DC',
    'Haricots Noirs': '#000000',
    'Potatoes': '#FFD700',
    'Couscous Perlé': '#F5DEB3',
    'Tortilla': '#F5DEB3',
    'Semoule': '#FFFACD',
    'Jambon': '#FFC0CB',
    'Pain pita': '#F5DEB3',
    'Canard': '#8B0000',
    'Blé': '#DEB887'
  };

  private week_number: number;

  constructor(private api: ApiService) {
    this.week_number = getISOWeek(new Date());
  }

  ngOnInit() {
    this.loadRecettes();
  }

  loadRecettes(): void {
    this.api.getRecettes().subscribe(data => {
      this._recettes = data;
    });
  }


  get recettes(): Recette[] {
    //return [...this._recettes].filter((recette) => this.week_number === this.getWeekNumber(recette.used));
    return this._recettes;
  }

  getCategoryColor(cat: string): string {
    return this.colors[cat] || '#ccc';
  }

  private getWeekNumber(date: Date | null): number {
    return date != null ? getISOWeek(date) : -1;
  }
}
