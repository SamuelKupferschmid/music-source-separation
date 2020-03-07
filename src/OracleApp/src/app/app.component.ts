import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from './data/data.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor(private router: Router, private dataService: DataService) {
  }

  public loadDataset(dataset: string) {
    this.dataService.loadDataset(dataset);
    const next = this.dataService.getNextSample();
    this.router.navigate([next]);
  }

  public download() {
    this.dataService.downloadDataset();
  }
}
