import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SwitchListComponent } from './switch-list.component';
import { RouterTestingModule } from '@angular/router/testing';
import { ApiModule } from '../api/api.module';

describe('SwitchListComponent', () => {
  let component: SwitchListComponent;
  let fixture: ComponentFixture<SwitchListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SwitchListComponent ]
      imports: [
        ApiModule,
        RouterTestingModule,
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SwitchListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
