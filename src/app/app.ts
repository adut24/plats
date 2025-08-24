import { Component, OnInit, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Topbar } from './topbar/topbar';
import { ApiService, Recette } from './services/api';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Topbar, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnInit {
  protected readonly title = signal('Recettes de la semaine');
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


  constructor(private api: ApiService) { }

  ngOnInit() {
    this.loadRecettes();
  }

  loadRecettes(): void {
    this.api.getRecettes().subscribe(data => {
      this._recettes = data;
    });
  }

  get recettes(): Recette[] {
    return this._recettes;
  }

  getCategoryColor(cat: string): string {
    return this.colors[cat] || '#ccc';
  }
}
