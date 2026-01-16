"""
Servicio de Facturación (Frontend)
"""
from typing import List, Dict, Any, Optional
from app.services.api_client import api_client
import os
import tempfile
import subprocess


class InvoiceService:
    """Servicio para gestionar facturas"""
    
    def get_all(self, skip: int = 0, limit: int = 100,
                status: Optional[str] = None,
                guest_id: Optional[int] = None,
                currency: Optional[str] = None,
                from_date: Optional[str] = None,
                to_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene todas las facturas"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if guest_id:
            params["guest_id"] = guest_id
        if currency:
            params["currency"] = currency
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        
        return api_client.get("/api/invoices/", params=params)
    
    def get_by_id(self, invoice_id: int) -> Dict[str, Any]:
        """Obtiene una factura por ID"""
        return api_client.get(f"/api/invoices/{invoice_id}")
    
    def create(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una factura"""
        return api_client.post("/api/invoices/", json_data=invoice_data)
    
    def generate_from_reservation(self, reservation_id: int, 
                                   include_payments: bool = True,
                                   guest_document_type: Optional[str] = None,
                                   guest_document_number: Optional[str] = None,
                                   guest_address: Optional[str] = None,
                                   notes: Optional[str] = None) -> Dict[str, Any]:
        """Genera una factura desde una reserva"""
        data = {
            "reservation_id": reservation_id,
            "include_payments": include_payments
        }
        if guest_document_type:
            data["guest_document_type"] = guest_document_type
        if guest_document_number:
            data["guest_document_number"] = guest_document_number
        if guest_address:
            data["guest_address"] = guest_address
        if notes:
            data["notes"] = notes
        
        return api_client.post("/api/invoices/generate", json_data=data)
    
    def update(self, invoice_id: int, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una factura"""
        return api_client.put(f"/api/invoices/{invoice_id}", json_data=invoice_data)
    
    def add_item(self, invoice_id: int, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Agrega un item a una factura"""
        return api_client.post(f"/api/invoices/{invoice_id}/items", json_data=item_data)
    
    def remove_item(self, invoice_id: int, item_id: int) -> Dict[str, Any]:
        """Elimina un item de una factura"""
        return api_client.delete(f"/api/invoices/{invoice_id}/items/{item_id}")
    
    def issue(self, invoice_id: int) -> Dict[str, Any]:
        """Emite una factura"""
        return api_client.put(f"/api/invoices/{invoice_id}/issue")
    
    def void(self, invoice_id: int) -> Dict[str, Any]:
        """Anula una factura"""
        return api_client.put(f"/api/invoices/{invoice_id}/void")
    
    def register_payment(self, invoice_id: int, amount: float) -> Dict[str, Any]:
        """Registra un pago en una factura"""
        return api_client.post(f"/api/invoices/{invoice_id}/payment", json_data={"amount": amount})
    
    def delete(self, invoice_id: int) -> Dict[str, Any]:
        """Elimina una factura"""
        return api_client.delete(f"/api/invoices/{invoice_id}")
    
    def download_pdf(self, invoice_id: int, filename: Optional[str] = None) -> str:
        """
        Descarga el PDF de una factura y lo abre.
        Retorna la ruta del archivo descargado.
        """
        response = api_client.get_raw(f"/api/invoices/{invoice_id}/pdf")
        
        if filename is None:
            filename = f"factura_{invoice_id}.pdf"
        
        # Guardar en directorio temporal
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Abrir el PDF con el visor predeterminado
        try:
            os.startfile(filepath)  # Windows
        except AttributeError:
            subprocess.run(['open', filepath])  # macOS
        except Exception:
            subprocess.run(['xdg-open', filepath])  # Linux
        
        return filepath
    
    def download_receipt_pdf(self, invoice_id: int, filename: Optional[str] = None) -> str:
        """
        Descarga el PDF de un recibo y lo abre.
        Retorna la ruta del archivo descargado.
        """
        response = api_client.get_raw(f"/api/invoices/{invoice_id}/receipt-pdf")
        
        if filename is None:
            filename = f"recibo_{invoice_id}.pdf"
        
        # Guardar en directorio temporal
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Abrir el PDF con el visor predeterminado
        try:
            os.startfile(filepath)  # Windows
        except AttributeError:
            subprocess.run(['open', filepath])  # macOS
        except Exception:
            subprocess.run(['xdg-open', filepath])  # Linux
        
        return filepath


# Instancia global
invoice_service = InvoiceService()
