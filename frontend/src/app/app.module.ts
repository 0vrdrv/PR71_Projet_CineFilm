// frontend/src/app/app.module.ts

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { FilmsComponent } from './pages/films/films.component';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { MovieDetailComponent } from './pages/movie-detail/movie-detail.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { MembersComponent } from './pages/members/members.component';
import { ListsComponent } from './pages/lists/lists.component';
import { ListDetailComponent } from './pages/list-detail/list-detail.component';
import { ToastComponent } from '../app/shared/components/toast/toast.component';
import { FeedComponent } from './pages/feed/feed.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    RegisterComponent,
    FilmsComponent,
    MovieDetailComponent,
    ProfileComponent,
    MembersComponent,
    ListsComponent,
    ListDetailComponent,
    ToastComponent,
    FeedComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }