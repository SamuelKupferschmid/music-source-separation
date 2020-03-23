import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private _headers: string[];
  private _columns: any[][];
  private _indieces: { [key: string]: number } = {};
  private _sampleCount: number;

  private _unlabeledSamples = new Set<string>();

  //private _estimationIndicies = [3, 4, 5];
  private _labelIndex = 2;
  private _keyIndex = 1;

  constructor() {

  }

  public loadDataset(dataset: string) {
    const sep = '\t';
    const lines = dataset.split('\n');
    this._headers = lines[0].split(sep);

    this._columns = [...Array(this._headers.length).keys()].map(() => []);

    for (let r = 1; r < lines.length; r++) {
      const values = lines[r].split(sep);
      const key = values[this._keyIndex];

      if(values[this._labelIndex] == '') {
        this._unlabeledSamples.add(key);
      }

      this._indieces[key] = r - 1;

      for (let c = 0; c < values.length; c++) {
        this._columns[c].push(values[c]);
      }
    }

    this._sampleCount = lines.length - 1;
  }

  public getFilepath(key: string) {
    const row = this._indieces[key];
    return this._columns[0][row] + '/' + this._columns[1][row];
  }

  public getNextSample(): string {
    for(const s of this._unlabeledSamples) {
      return s;
    }
  }

  public setLabel(key: string, labelIndex: number) {
    const row = this._indieces[key];
    this._columns[this._labelIndex][row] = labelIndex;

    this._unlabeledSamples.delete(key);
  }

  public downloadDataset() {
    const sep = '\t';
    let output = this._headers.join(sep);

    for (let row = 0; row < this._sampleCount; row++) {
      output += '\n' + this._columns.map(col => col[row]).join(sep);
    }
    const blob = new Blob([output], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    window.open(url);
  }
}
