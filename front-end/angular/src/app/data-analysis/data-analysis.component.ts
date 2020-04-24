import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-data-analysis',
  templateUrl: './data-analysis.component.html',
  styleUrls: ['./data-analysis.component.scss'],
})
export class DataAnalysisComponent implements OnInit {
  title = 'Datenanalyse';
  rawFileString: string;
  fileLines: string[];
  seed: string;
  fileUploaded = false;

  data: {
    voltage: number;
    power: number;
    time: string;
    channel: string;
  }[] = [];

  labels: string[] = [];
  constructor() {}

  ngOnInit(): void {}

  onFileInput(event) {
    this.fileUploaded = true;
    const file = event.target.files[0];
    const fileReader = new FileReader();
    fileReader.onload = (e) => {
      this.rawFileString = fileReader.result as string;
      this.fileLines = this.rawFileString.split(/\r\n/g);
      this.title = `Messung vom ${this.fileLines[0]
        .split('-')
        .slice(1, 4)
        .join('.')}`;
      this.seed = this.fileLines[0].split('-')[0];
      this.fileLines.splice(0, 1);
      console.log(this.fileLines[0]);
      // 0.2991|299.10156|04/22/2020|21:38:48.593538|1
      this.data = this.fileLines.map((line: string) => {
        const items = line.split('|');
        this.labels.push(items[2]);
        return {
          voltage: Number(items[0]),
          power: Number(items[1]),
          time: items[3],
          channel: items[4],
        };
      });
      console.log(this.fileLines.splice(0, 1));
    };
    fileReader.readAsText(file);
  }
}
