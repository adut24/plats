import { Routes } from '@angular/router';
import { NextWeek } from './pages/next-week/next-week';
import { Current } from './pages/current/current';
import { LastMonth } from './pages/last-month/last-month';

export const routes: Routes = [
    { path: '', component: Current },
    { path: 'next-week', component: NextWeek },
    { path: 'last-month', component: LastMonth }
];
