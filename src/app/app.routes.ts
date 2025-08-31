import { Routes } from '@angular/router';
import { All } from './pages/all/all';
import { Current } from './pages/current/current';
import { LastMonth } from './pages/last-month/last-month';
import { NextWeek } from './pages/next-week/next-week';
import { Recipe } from './pages/recipe/recipe';

export const routes: Routes = [
    { path: '', component: Current },
    { path: 'next-week', component: NextWeek },
    { path: 'last-month', component: LastMonth },
    { path: 'recipe/:id', component: Recipe },
    { path: 'all', component: All }
];
