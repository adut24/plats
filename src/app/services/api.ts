import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Recette {
  id: string;
  nom: string;
  used: Date | null;
  categories: string[];
  image_path: string;
  created_at: Date;
  updated_at: Date;
}

export interface RecetteDTO {
  id: string;
  nom: string;
  used: string | null;
  categories: string[];
  image_path: string;
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getRecettes(): Observable<Recette[]> {
    return this.http.get<{ [key: string]: RecetteDTO }>(`${this.baseUrl}/recettes`).pipe(
      map((recettesObj: { [key: string]: RecetteDTO }) =>
        Object.values(recettesObj).map(this.toRecette)
      )
    );
  }

  getRecette(id: string): Observable<Recette> {
    return this.http.get<RecetteDTO>(`${this.baseUrl}/recettes/${id}`).pipe(
      map(this.toRecette));
  }

  updateUsageTrue(id: string): Observable<Recette> {
    return this.http.put<RecetteDTO>(`${this.baseUrl}/used-true/${id}`, null).pipe(
      map(this.toRecette));
  }

  updateUsageFalse(id: string): Observable<Recette> {
    return this.http.put<RecetteDTO>(`${this.baseUrl}/used-false/${id}`, null).pipe(
      map(this.toRecette));
  }

  toRecette(dto: RecetteDTO): Recette {
    return {
      ...dto,
      used: dto.used ? new Date(dto.used) : null,
      created_at: new Date(dto.created_at),
      updated_at: new Date(dto.updated_at)
    };
  }
}
