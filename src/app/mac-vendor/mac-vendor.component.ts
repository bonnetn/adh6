import { Component, OnInit, OnDestroy, Input } from '@angular/core';

import { HttpClient, HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-mac-vendor',
  templateUrl: './mac-vendor.component.html',
  styleUrls: ['./mac-vendor.component.css']
})
export class MacVendorComponent implements OnInit, OnDestroy {

  @Input() mac: string;

  vendor: string = "Searching...";
  private alive: boolean = true;

  constructor(
    private http: HttpClient,
  ) { }

  ngOnInit() {
    this.http.get( "https://api.macvendors.com/" + this.mac, {
      responseType: "text"
    })
      .takeWhile( () => this.alive )
      .subscribe(( data:string) => {
        this.vendor = data;
      },
        ( err : HttpErrorResponse) => {
          this.vendor = "Unknown";
        });
  }

  ngOnDestroy() {
    this.alive = false;
  }

}
