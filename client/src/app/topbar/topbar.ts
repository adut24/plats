import { Component, ElementRef, HostListener, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { ApiService, Recette } from '../services/api';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [RouterModule, CommonModule, FormsModule],
  templateUrl: './topbar.html',
  styleUrls: ['./topbar.scss']
})
export class Topbar implements OnInit {
  query: string = '';
  results: Recette[] = [];
  allRecettes: Recette[] = [];

  private searchSubject = new Subject<string>();

  constructor(private api: ApiService,
    private router: Router,
    private el: ElementRef) { }

  ngOnInit() {
    this.api.getRecettes().subscribe(recettes => {
      this.allRecettes = recettes;
    });

    this.searchSubject.pipe(
      debounceTime(300),
      distinctUntilChanged()
    )
      .subscribe(() => this.filterResults());
  }

  onSearch() {
    this.searchSubject.next(this.query);
  }

  private filterResults() {
    const q = this.query.trim()
      .toLowerCase();
    if (!q) {
      this.results = [];
    } else {
      this.results = this.allRecettes.filter(r =>
        r.nom.toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .includes(q)
      );
    }
  }

  goToRecipe(id: string) {
    this.results = [];
    this.query = '';
    this.router.navigate(['/recipe', id]);
  }

  @HostListener('document:click', ['$event'])
  onClickOutside(event: MouseEvent) {
    if (!this.el.nativeElement.contains(event.target)) {
      this.results = [];
    }
  }
}
