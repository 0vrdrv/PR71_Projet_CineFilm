import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { FilmsComponent } from './pages/films/films.component';
import { MovieDetailComponent } from './pages/movie-detail/movie-detail.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { MembersComponent } from './pages/members/members.component';
import { AuthGuard } from './guards/auth.guard';
import { ListsComponent } from './pages/lists/lists.component';
import { ListDetailComponent } from './pages/list-detail/list-detail.component';
import { FeedComponent } from './pages/feed/feed.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'films', component: FilmsComponent },
  { path: 'films/:id', component: MovieDetailComponent },
  { path: 'members', component: MembersComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'profile/:id', component: ProfileComponent },
  { path: 'lists', component: ListsComponent },
  { path: 'lists/:id', component: ListDetailComponent },
  { path: '**', redirectTo: '' },
  { path: 'feed', component: FeedComponent, canActivate: [AuthGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
