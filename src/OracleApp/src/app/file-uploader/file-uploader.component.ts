import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { DataService } from '../data/data.service';

@Component({
  selector: 'app-file-uploader',
  templateUrl: './file-uploader.component.html',
  styleUrls: ['./file-uploader.component.scss']
})
export class FileUploaderComponent implements OnInit {

  constructor() { }

  @Output() textLoaded = new EventEmitter<string>();

  ngOnInit(): void {
  }

  change(target: HTMLInputElement) {
    const reader = new FileReader();
    reader.onloadend = ev => {
      this.textLoaded.emit(<string>ev.target.result)
    };

    reader.readAsText(target.files.item(0))
    console.log(event)
  }

}
