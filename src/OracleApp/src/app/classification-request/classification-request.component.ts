import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { map } from 'rxjs/operators'
import { Observable } from 'rxjs';
import { SafeResourceUrl, DomSanitizer } from '@angular/platform-browser';
import { DataService } from '../data/data.service';
import { MatButtonToggleChange } from '@angular/material/button-toggle';

@Component({
  selector: 'app-classification-request',
  templateUrl: './classification-request.component.html',
  styleUrls: ['./classification-request.component.scss']
})
export class ClassificationRequestComponent implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router, private dataService: DataService, private sanitizer: DomSanitizer) { }

  public id$: Observable<string>;
  public url$: Observable<SafeResourceUrl>;
  public selected: any;

  ngOnInit(): void {
    this.id$ = this.route.paramMap.pipe(map(params => params.get('id')));

    this.id$.subscribe(()=> {
      this.selected = null;
    })

    this.url$ = this.id$.pipe(
      map(id => this.sanitizer.bypassSecurityTrustResourceUrl('http://localhost:8080/' + this.dataService.getFilepath(id)))
    )
  }

  public setLabel(key: string, event: MatButtonToggleChange) {
    this.dataService.setLabel(key, Number.parseInt(event.value));

    const next = this.dataService.getNextSample();
    this.router.navigate([next]);

  }

}
