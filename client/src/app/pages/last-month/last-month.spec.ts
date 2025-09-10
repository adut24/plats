import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LastMonth } from './last-month';

describe('LastMonth', () => {
  let component: LastMonth;
  let fixture: ComponentFixture<LastMonth>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LastMonth]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LastMonth);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
