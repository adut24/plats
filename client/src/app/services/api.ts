import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Recette {
  id: string;
  nom: string;
  used: Date | null;
  categories: string[];
  image_path: string;
  temps_total: string;
  steps: string[];
  steps_text_path: string;
  ingredients: string;
}

export interface RecetteDTO {
  id: string;
  nom: string;
  used: string | null;
  categories: string[];
  image_path: string;
  ingredients: string;
  temps_total: string;
  steps: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getRecettes(): Observable<Recette[]> {
    return this.http.get<{ [key: string]: RecetteDTO }>(
      `${this.baseUrl}/recettes`).pipe(
        map((recettesObj) =>
          Object.values(recettesObj).map(this.toRecette)
        )
      );
  }

  getRecette(id: string): Observable<Recette> {
    return this.http.get<RecetteDTO>(`${this.baseUrl}/recettes/${id}`)
      .pipe(
        map(this.toRecette));
  }

  updateUsageTrue(id: string): Observable<Recette> {
    return this.http.put<RecetteDTO>(`${this.baseUrl}/used-true/${id}`, null)
      .pipe(
        map(this.toRecette));
  }

  updateUsageFalse(id: string): Observable<Recette> {
    return this.http.put<RecetteDTO>(`${this.baseUrl}/used-false/${id}`, null)
      .pipe(
        map(this.toRecette));
  }

  toRecette(dto: RecetteDTO): Recette {
    const steps = dto.steps.slice(0, -1);
    return {
      ...dto,
      used: dto.used ? new Date(dto.used) : null,
      steps: steps,
      steps_text_path: dto.steps[dto.steps.length - 1]
    };
  }
}
