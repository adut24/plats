import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService, Recette } from '../../services/api';
import { Observable, firstValueFrom } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-recipe',
  imports: [AsyncPipe],
  templateUrl: './recipe.html',
  styleUrl: './recipe.scss'
})
export class Recipe implements OnInit {
  private readonly recette$!: Observable<Recette>;
  ingredients: [string, string[]][] = [];
  columns: [string, string[]][][] = [];

  constructor(private route: ActivatedRoute,
    private api: ApiService,
    private http: HttpClient) {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.recette$ = this.api.getRecette(id);
    }
  }

  async ngOnInit() {
    const recette = await firstValueFrom(this.recette$);
    const content = await firstValueFrom(
      this.http.get(recette.ingredients, { responseType: 'text' })
    );
    this.ingredients = this.parseIngredients(content);
    this.columns = this.splitIntoColumns(this.ingredients, 3);
  }

  get recette(): Observable<Recette> {
    return this.recette$;
  }

  private parseIngredients(content: string): [string, string[]][] {
    return content
      .split('\n')
      .filter(line => line.trim().length > 0)
      .map(line => {
        const [quantite, ...ingredient] = line.split(' | ');
        return [quantite.substring(8, quantite.length), ingredient];
      });
  }

  private splitIntoColumns<T>(arr: T[], numCols: number): T[][] {
    const cols: T[][] = Array.from({ length: numCols }, () => []);
    arr.forEach((item, index) => {
      cols[index % numCols].push(item);
    });
    return cols.filter(col => col.length > 0);
  }
}
