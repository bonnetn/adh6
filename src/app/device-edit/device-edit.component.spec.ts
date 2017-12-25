import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceEditComponent } from './device-edit.component';
import { ReactiveFormsModule } from '@angular/forms';

import { ApiModule } from '../api/api.module';
import { RouterTestingModule } from '@angular/router/testing';


describe('DeviceEditComponent', () => {
  let component: DeviceEditComponent;
  let fixture: ComponentFixture<DeviceEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeviceEditComponent ],
      imports: [ 
        ReactiveFormsModule, 
        RouterTestingModule,
        ApiModule,
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeviceEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
