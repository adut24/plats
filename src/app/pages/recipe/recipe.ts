import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService, Recette } from '../../services/api';
import { Observable } from 'rxjs';
import { AsyncPipe } from '@angular/common';

@Component({
  selector: 'app-recipe',
  imports: [AsyncPipe],
  templateUrl: './recipe.html',
  styleUrl: './recipe.scss'
})
export class Recipe {
  recette$!: Observable<Recette>;

  constructor(private route: ActivatedRoute, private api: ApiService) {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.recette$ = this.api.getRecette(id);
    }
  }
}
