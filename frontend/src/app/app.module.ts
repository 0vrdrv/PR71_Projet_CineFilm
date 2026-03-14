// frontend/src/app/app.module.ts

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
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
import { SkeletonComponent } from './shared/components/skeleton/skeleton.component';
import { FeedComponent } from './pages/feed/feed.component';
import { TruncatePipe } from './pipes/truncate.pipe';
import { StarDisplayPipe } from './pipes/star-display.pipe';
import { SharedModule } from './shared/shared.module';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { ActivityComponent } from './pages/activity/activity.component';
import { SearchComponent } from './pages/search/search.component';
import { ConfirmModalComponent } from './shared/components/confirm-modal/confirm-modal.component';

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
    SkeletonComponent,
    FeedComponent,
    TruncatePipe,
    StarDisplayPipe,
    NotFoundComponent,
    ActivityComponent,
    SearchComponent,
    ConfirmModalComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    SharedModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
