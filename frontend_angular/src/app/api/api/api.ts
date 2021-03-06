export * from './account.service';
import { AccountService } from './account.service';
export * from './accountType.service';
import { AccountTypeService } from './accountType.service';
export * from './device.service';
import { DeviceService } from './device.service';
export * from './member.service';
import { MemberService } from './member.service';
export * from './membership.service';
import { MembershipService } from './membership.service';
export * from './paymentMethod.service';
import { PaymentMethodService } from './paymentMethod.service';
export * from './port.service';
import { PortService } from './port.service';
export * from './product.service';
import { ProductService } from './product.service';
export * from './room.service';
import { RoomService } from './room.service';
export * from './switch.service';
import { SwitchService } from './switch.service';
export * from './temporaryAccount.service';
import { TemporaryAccountService } from './temporaryAccount.service';
export * from './transaction.service';
import { TransactionService } from './transaction.service';
export const APIS = [AccountService, AccountTypeService, DeviceService, MemberService, MembershipService, PaymentMethodService, PortService, ProductService, RoomService, SwitchService, TemporaryAccountService, TransactionService];
