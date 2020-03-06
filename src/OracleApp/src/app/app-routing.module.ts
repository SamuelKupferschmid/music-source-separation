import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { ClassificationRequestComponent } from './classification-request/classification-request.component';


const routes: Routes = [{
  path:'',
  children: [
    {path: ':id', component: ClassificationRequestComponent }
  ]
}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
