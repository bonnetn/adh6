import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MacVendorComponent } from './mac-vendor.component';

describe('MacVendorComponent', () => {
  let component: MacVendorComponent;
  let fixture: ComponentFixture<MacVendorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MacVendorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MacVendorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
